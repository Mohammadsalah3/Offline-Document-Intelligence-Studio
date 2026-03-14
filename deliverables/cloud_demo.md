# Cloud Demo

A lightweight cloud demo of the project is available on Hugging Face:

https://huggingface.co/spaces/Mohdisleem3/offline-document-intelligence

## Note

This deployment is intended as a demonstration version of the system.

After several experiments and attempts, I was able to resolve the machine learning component by training and using a much smaller model so it could run within the constraints of the free Hugging Face environment.

However, running the **local LLM through Ollama** was not feasible in this environment. The smallest available models in Ollama (such as Gemma) are approximately **280 MB**, which is significantly larger than the storage and resource limits allowed in the free Hugging Face Space.

I also experimented with alternative approaches, such as using the Hugging Face `transformers` pipeline with very small models. While this allowed the endpoint to technically run, the generated responses were extremely poor and did not meaningfully represent the intended functionality of the system.

Therefore, the cloud demo focuses on demonstrating the **system architecture and core capabilities** rather than full-scale LLM performance.

The **complete system**, including the fully functional local LLM and all features, is available in the **local version provided in this repository**, where the application runs without the limitations of the free cloud environment.

I hope this explanation clarifies the technical constraints encountered during deployment and demonstrates the intended skills and implementation behind the project.

Thank you.
