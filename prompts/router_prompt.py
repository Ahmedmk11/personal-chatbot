from langchain_core.prompts import PromptTemplate

router_prompt = PromptTemplate(
    input_variables=["input"],
    template="""
You are an expert assistant routing user queries to the correct chain.
The available chains are:

- "redirect": for questions about GitHub, portfolio, LinkedIn, email, resume, contact info or questions about links within the portfolio website or for project links like github repo, live demo or research paper.
- "retrieval": for questions that need details from Ahmed's CV, projects, portfolio sections or skills.
- "conversation": for casual conversation.

Decide which chain the query belongs to. Respond with exactly one of: redirect, retrieval, or conversation.

User query: {input}
Chain:
"""
)
