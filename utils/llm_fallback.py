from langchain_core.runnables import RunnableLambda

def with_fallback(primary_llm, fallback_llm, prompt, parser=True):    
    async def run_with_fallback(inputs, config=None):
        primary_chain = prompt | primary_llm
        fallback_chain = prompt | fallback_llm
        
        try:
            async for chunk in primary_chain.astream(inputs, config=config or {}):
                if hasattr(chunk, 'content'):
                    yield chunk.content
                else:
                    yield str(chunk)
        except Exception as e:
            print(f"Primary model failed, falling back: {e}")
            async for chunk in fallback_chain.astream(inputs, config=config or {}):
                if hasattr(chunk, 'content'):
                    yield chunk.content
                else:
                    yield str(chunk)
    
    return RunnableLambda(run_with_fallback)
