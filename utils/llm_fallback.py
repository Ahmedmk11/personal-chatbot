from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def with_fallback(primary_llm, fallback_llm, prompt, parser=True):
    def _runner(inputs, config):
        try:
            if parser:
                return (prompt | primary_llm | StrOutputParser()).invoke(inputs, config=config)
            return (prompt | primary_llm).invoke(inputs, config=config)
        except Exception as e:
            print(f"Primary model failed, falling back: {e}")
            if parser:
                return (prompt | fallback_llm | StrOutputParser()).invoke(inputs, config=config)
            return (prompt | fallback_llm).invoke(inputs, config=config)
    return RunnableLambda(_runner)
