-- ============================================================================
-- SUPABASE RAG SETUP
-- Run this SQL in your Supabase SQL Editor
-- ============================================================================

-- Enable the pgvector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================================
-- CREATE DOCUMENTS TABLE (if not exists)
-- ============================================================================

-- Note: Your table already exists from n8n setup
-- This is for reference and verification

-- If you need to create it fresh, use:
/*
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(768)  -- Gemini embedding-001 outputs 768 dimensions
);
*/

-- ============================================================================
-- VERIFY YOUR TABLE STRUCTURE
-- ============================================================================

-- Check if table exists and view structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'documents';

-- ============================================================================
-- CREATE INDEX FOR VECTOR SIMILARITY SEARCH
-- ============================================================================

-- Create an index for faster vector similarity search using HNSW algorithm
-- This significantly speeds up similarity searches
CREATE INDEX IF NOT EXISTS documents_embedding_idx 
ON documents 
USING hnsw (embedding vector_cosine_ops);

-- Alternative: Use IVFFlat index (good for smaller datasets)
-- CREATE INDEX IF NOT EXISTS documents_embedding_idx 
-- ON documents 
-- USING ivfflat (embedding vector_cosine_ops)
-- WITH (lists = 100);

-- ============================================================================
-- CREATE SIMILARITY SEARCH FUNCTION
-- ============================================================================

-- This function performs similarity search using cosine distance
-- It returns the most similar documents to the query embedding

CREATE OR REPLACE FUNCTION match_documents(
    query_embedding VECTOR(768),
    match_count INT DEFAULT 5,
    filter JSONB DEFAULT '{}'::jsonb
)
RETURNS TABLE (
    id BIGINT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        documents.id,
        documents.content,
        documents.metadata,
        1 - (documents.embedding <=> query_embedding) AS similarity
    FROM documents
    WHERE (filter = '{}'::jsonb OR documents.metadata @> filter)
    ORDER BY documents.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ============================================================================
-- GRANT PERMISSIONS (if needed)
-- ============================================================================

-- Grant permissions to authenticated users
-- GRANT SELECT, INSERT, UPDATE, DELETE ON documents TO authenticated;
-- GRANT EXECUTE ON FUNCTION match_documents TO authenticated;

-- For service role (recommended for backend operations)
-- GRANT ALL ON documents TO service_role;
-- GRANT EXECUTE ON FUNCTION match_documents TO service_role;

-- ============================================================================
-- TEST THE SETUP
-- ============================================================================

-- Check total documents
SELECT COUNT(*) as total_documents FROM documents;

-- View sample documents
SELECT id, LEFT(content, 100) as content_preview, metadata 
FROM documents 
LIMIT 5;

-- Test the match function (will work after you insert some data)
-- SELECT * FROM match_documents(
--     (SELECT embedding FROM documents LIMIT 1),
--     5
-- );

-- ============================================================================
-- UTILITY QUERIES
-- ============================================================================

-- Delete all documents (BE CAREFUL!)
-- DELETE FROM documents;

-- Delete documents from specific source
-- DELETE FROM documents WHERE metadata->>'source' = 'your_file.pdf';

-- Count documents by source
SELECT 
    metadata->>'source' as source_file,
    COUNT(*) as num_chunks
FROM documents
GROUP BY metadata->>'source'
ORDER BY num_chunks DESC;

-- ============================================================================
-- NOTES
-- ============================================================================

/*
IMPORTANT POINTS:

1. VECTOR DIMENSIONS:
   - Gemini embedding-001 outputs 768-dimensional vectors
   - Make sure your embedding column is VECTOR(768)
   - If using different embedding model, adjust dimensions

2. SIMILARITY METRICS:
   - <=> : Cosine distance (default, recommended)
   - <-> : L2 distance (Euclidean)
   - <#> : Inner product

3. INDEX TYPES:
   - HNSW: Better for larger datasets, faster queries
   - IVFFlat: Good for smaller datasets, faster indexing

4. PERFORMANCE:
   - HNSW is recommended for production use
   - Adjust 'lists' parameter in IVFFlat based on dataset size
   - Rule of thumb: lists = sqrt(number_of_rows)

5. METADATA FILTERING:
   - You can filter by source, page, or any metadata field
   - Use JSONB operators: @>, ->, ->>

EXAMPLE USAGE FROM PYTHON:

# Search with filter
result = supabase.rpc(
    'match_documents',
    {
        'query_embedding': embedding,
        'match_count': 5,
        'filter': {'source': 'my_document.pdf'}
    }
).execute()
*/
