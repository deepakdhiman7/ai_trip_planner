from utils.model_loader import ModelLoader


loader = ModelLoader()
llm = loader.load_llm()

output = llm.invoke("what is capex meaning?")

print(output)