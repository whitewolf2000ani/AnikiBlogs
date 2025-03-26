---
title: Implementing Open LLM Models with JAX and Flax
date: 2025-03-21
---

---
Before diving into the implementation details, 
I want to summarize our approach: 
we'll be creating JAX/Flax implementations of popular open-source LLM architectures, documenting everything thoroughly, and providing clear notebooks to demonstrate their usage. 
## Project Overview

JAX, combined with Flax, provides a powerful framework for implementing high-performance neural networks with benefits like JIT compilation, automatic differentiation, and excellent hardware acceleration support. Our goal is to create clean, well-documented implementations of open-source LLM architectures that can serve as reference material and starting points for further research.

## Implementation Roadmap

### Phase 1: Environment Setup and Core Components 

1. **Development Environment Setup**
    - Install JAX with hardware-specific optimizations (GPU/TPU)
    - Install Flax, Optax (optimizers), and supporting libraries
    - Configure development environment with appropriate compute resources
2. **Implement Core Architecture Components**
    - Token embedding layers
    - Various positional encoding mechanisms (sinusoidal, learned, rotary)
    - Attention mechanisms (multi-head attention with causal masking)
    - Feed-forward networks
    - Normalization layers (LayerNorm, RMSNorm)
    - Complete transformer blocks
    - Model definition classes with initialization and forward functions

### Phase 2: Model Implementations 

We'll implement several open-source LLM architectures, starting with simpler models and progressing to more complex ones:

1. **GPT-2 Style Model**
    - Decoder-only transformer architecture
    - LayerNorm and learned positional embeddings
    - Support for various model sizes (124M to 1.5B parameters)
2. **Gemma Architecture**
    - Google's efficient model developed specifically with JAX/Flax
    - RMSNorm and rotary positional embeddings
    - 2B and 7B parameter configurations
3. **Additional Models (Time Permitting)**
    - OpenLLaMA (open-source implementation of LLaMA)
    - Mistral (with mixture-of-experts layers)

For each model, we'll implement:

- Complete model definition classes
- Initialization from scratch and from pre-trained weights
- Forward pass functions optimized with JAX transformations
- Text generation utilities


### Phase 3: Utility Functions and Optimization 

1. **Weight Loading Utilities**
    - Parameter key remapping between different naming schemes
    - Shape and data type conversion utilities
    - Loading from HuggingFace model repositories
    - Checkpoint saving/loading with Orbax
2. **Inference and Generation**
    - Greedy decoding implementation
    - Sampling-based generation with temperature control
    - Top-k and top-p (nucleus) sampling
    - Batched inference support
3. **Performance Optimization**
    - JIT compilation for faster inference
    - Vectorization with vmap for batched processing
    - Device parallelism with pmap for multi-GPU/TPU setups
    - Memory optimization techniques like gradient checkpointing
    - Mixed precision support (bfloat16/fp16)

### Phase 4: Validation and Documentation 

1. **Validation Against Reference Implementations**
    - Compare outputs with HuggingFace reference models
    - Validate hidden states and logits using similarity metrics
    - Verify tokenizer consistency
    - Test text generation capabilities
2. **Documentation and Notebooks**
    - Comprehensive model documentation
    - Jupyter notebooks demonstrating usage
    - Performance benchmarks
    - Best practices for working with JAX/Flax models

## Technical Challenges and Solutions

### API Compatibility

Flax is transitioning from the Linen API to the newer NNX API. We'll need to handle compatibility by:

1. Using the flax.nnx.bridge API to convert between Linen and NNX modules
2. Properly handling RNG keys and variable collections
3. Testing thoroughly to ensure compatibility with different versions

### Memory Management for Large Models

For larger models, we'll implement:

1. Gradient checkpointing to reduce memory usage during training
2. Model parallelism strategies using JAX's device mesh and partition specs
3. Efficient parameter handling to minimize memory overhead

### Performance Optimization

To achieve optimal performance, we'll:

1. Use JAX's transformation functions (jit, vmap, pmap) appropriately
2. Apply XLA optimizations through JAX
3. Implement custom kernels where necessary using jax.lax operations
4. Leverage scan for sequential operations

## Repository Structure

```
jax-flax-llms/
├── models/
│   ├── components.py (shared transformer components)
│   ├── gpt2/
│   │   ├── model.py (model definition)
│   │   ├── config.py (model configuration)
│   │   └── utils.py (model-specific utilities)
│   ├── gemma/
│   │   ├── model.py
│   │   ├── config.py
│   │   └── utils.py
│   └── ...
├── utils/
│   ├── loading.py (weight loading utilities)
│   ├── generation.py (text generation functions)
│   ├── optimization.py (performance optimization)
│   └── validation.py (validation against references)
├── notebooks/
│   ├── 01_gpt2_tutorial.ipynb
│   ├── 02_gemma_tutorial.ipynb
│   └── ...
├── tests/
│   ├── test_components.py
│   ├── test_gpt2.py
│   ├── test_gemma.py
│   └── ...
├── requirements.txt
└── README.md
```


## Implementation Approach for Each Model

For each model (using GPT-2 as an example):

1. **Architecture Research**
    - Study the original architecture in detail
    - Identify key components and parameter configurations
    - Understand tokenization and preprocessing requirements
2. **Core Implementation**
    - Define the model class structure
    - Implement all necessary layers and components
    - Create forward pass function with JAX optimizations
3. **Weight Loading**
    - Create mapping between original weights and our implementation
    - Implement conversion functions for loading pre-trained weights
    - Test with published checkpoints
4. **Inference and Generation**
    - Implement text generation capabilities
    - Optimize for inference speed using JAX transformations
    - Support various decoding strategies
5. **Documentation and Examples**
    - Create comprehensive model documentation
    - Develop clear notebooks showing initialization, loading, and generation
    - Include performance benchmarks

## Tools and Dependencies

1. **Core Libraries**
    - JAX and JAXLIB (with GPU/TPU support)
    - Flax (neural network library)
    - Optax (optimizers)
    - Orbax (checkpointing)
2. **Support Libraries**
    - Transformers (for reference models and tokenizers)
    - NumPy and SciPy (numerical computing)
    - Matplotlib (visualization)
3. **Development Tools**
    - Jupyter notebooks (for examples and demonstrations)
    - PyTest (for testing)
    - GitHub (for version control and publication)

## Educational Focus

Since this project is primarily educational, we'll emphasize:

1. **Clear, Well-Documented Code**
    - Comprehensive docstrings
    - Explanatory comments for complex sections
    - Consistent style and naming conventions
2. **Conceptual Understanding**
    - Explain architecture decisions in documentation
    - Compare implementation choices with original models
    - Highlight JAX/Flax-specific optimizations
3. **Practical Examples**
    - Step-by-step notebooks for different use cases
    - Performance comparison between optimization strategies
    - Tips and best practices for working with JAX/Flax

## Conclusion

This project will create a valuable educational resource for researchers and developers interested in implementing LLMs with JAX and Flax. By providing clear, optimized implementations of popular open-source architectures, along with comprehensive documentation and examples, we'll help bridge the gap between theoretical understanding and practical implementation.

The end result will be a GitHub repository showcasing these implementations, ready for others to use as reference material or starting points for their own research and experimentation.

<div style="text-align: center">⁂</div>

[^1]: https://cloud.google.com/blog/products/ai-machine-learning/guide-to-jax-for-pytorch-developers

[^2]: https://www.upwork.com/resources/google-jax

[^3]: https://rocm.blogs.amd.com/artificial-intelligence/distributed-sft-jax/README.html

[^4]: https://www.newhorizons.com/resources/blog/jax-vs-pytorch-comparing-two-deep-learning-frameworks

[^5]: https://docs.jax.dev/en/latest/quickstart.html

[^6]: https://en.wikipedia.org/wiki/JAX_(software)

[^7]: https://www.reddit.com/r/LocalLLaMA/comments/1aw9ukl/a_jax_based_library_for_training_finetuning_and/

[^8]: https://www.reddit.com/r/MachineLearning/comments/1b08qv6/d_is_it_worth_switching_to_jax_from/

[^9]: https://www.youtube.com/watch?v=e8StU6WQCqw

[^10]: https://www.youtube.com/watch?v=dYiJunh9DSk

[^11]: https://flax.readthedocs.io/en/latest/guides/bridge_guide.html

[^12]: https://flax.readthedocs.io/en/v0.8.1/

[^13]: https://github.com/google/flaxformer

[^14]: https://flax.readthedocs.io

[^15]: https://gonzoml.substack.com/p/jax-things-to-watch-for-in-2025

[^16]: https://flax.readthedocs.io/en/latest/examples/core_examples.html

[^17]: https://rocm.blogs.amd.com/artificial-intelligence/nanoGPT-JAX/README.html

[^18]: https://flax.readthedocs.io/en/latest/mnist_tutorial.html

[^19]: https://github.com/nlsfnr/MiniGPT

[^20]: https://docs.jaxstack.ai/en/latest/JAX_for_LLM_pretraining.html

[^21]: https://docs.jaxstack.ai/en/stable/getting_started_with_jax_for_AI.html

[^22]: https://docs.bentoml.com/en/latest/reference/bentoml/frameworks/flax.html

[^23]: https://github.com/mgrankin/minGPT

[^24]: https://github.com/dhyaneesh/awesome-jax-flax-llms

[^25]: https://blog.google/technology/developers/gemma-open-models/

[^26]: https://huggingface.co/docs/diffusers/en/using-diffusers/stable_diffusion_jax_how_to

[^27]: https://cloud.google.com/vertex-ai/generative-ai/docs/open-models/use-open-models

[^28]: https://huggingface.co/blog/gemma

[^29]: https://flax.readthedocs.io/en/latest/guides/training_techniques/transfer_learning.html

[^30]: https://www.lakera.ai/blog/open-source-llms

[^31]: https://flax-linen.readthedocs.io/en/latest/developer_notes/module_lifecycle.html

[^32]: https://mint.westdri.ca/ai/jx/fl_model

[^33]: https://flax.readthedocs.io/en/latest/developer_notes/lift.html

[^34]: https://wandb.ai/jax-series/simple-training-loop/reports/Writing-a-Training-Loop-in-JAX-and-Flax--VmlldzoyMzA4ODEy

[^35]: https://d2l.ai/chapter_attention-mechanisms-and-transformers/self-attention-and-positional-encoding.html

[^36]: https://theaisummer.com/jax/

[^37]: https://jax.readthedocs.io/en/latest/developer.html

[^38]: https://www.nvidia.com/en-us/on-demand/session/gtc24-s62246/

[^39]: https://becominghuman.ai/google-jax-vs-pytorch-vs-tensorflow-which-is-the-best-framework-for-machine-learning-eab6fc84de5d

[^40]: https://www.youtube.com/watch?v=uySOfXq-II0

[^41]: https://docs.jax.dev

[^42]: https://github.com/salesforce/jaxformer

[^43]: https://softwaremill.com/ml-engineer-comparison-of-pytorch-tensorflow-jax-and-flax/

[^44]: https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/JAX/tutorial2/Introduction_to_JAX.html

[^45]: https://github.com/google/jax/blob/main/docs/index.rst

[^46]: https://docs.jaxstack.ai/en/latest/examples.html

[^47]: https://www.it-jim.com/blog/jax-can-it-beat-pytorch-and-tensorflow/

[^48]: https://phlippe.github.io/media/GDE_Talk_Intro_to_JAX_Flax_2022_12_06.pdf

[^49]: https://flax.readthedocs.io/en/v0.8.3/experimental/nnx/index.html

[^50]: https://github.com/google/flax/issues/4045

[^51]: https://www.comet.com/site/blog/tracking-jax-and-flax-models-with-comet/

[^52]: https://flax.readthedocs.io/en/v0.5.3/design_notes/linen_design_principles.html

[^53]: https://www.reddit.com/r/MachineLearning/comments/1313cqj/p_introducing_nnx_neural_networks_for_jax/

[^54]: https://www.reddit.com/r/JAX/comments/1gpbbdy/flax_whats_your_thoughts_about_changing_linen_nnx/

[^55]: https://github.com/google/flax/blob/main/examples/lm1b/models.py

[^56]: https://github.com/google/flax

[^57]: https://www.youtube.com/watch?v=GNLOa4riys8

[^58]: https://hemptique.com/pages/flax-vs-linen-explained

[^59]: https://flax.readthedocs.io/en/v0.8.3/quick_start.html

[^60]: https://github.com/brentyi/minGPT-flax

[^61]: https://github.com/google/flax/blob/main/docs/index.rst

[^62]: https://docs.jaxstack.ai/en/latest/getting_started_with_jax_for_AI.html

[^63]: https://flax.readthedocs.io/en/latest/examples/index.html

[^64]: https://www.youtube.com/watch?v=vKcA094FSMk\&vl=en

[^65]: https://github.com/dieterichlawson/mingpt-jax

[^66]: https://flax.readthedocs.io/_/downloads/en/v0.6.10/pdf/

[^67]: https://github.com/karpathy/minGPT

[^68]: https://www.linkedin.com/posts/dogukantuna_github-dtunaixlstm-jax-jax-implementation-activity-7200894543347519489-FCbi

[^69]: https://ai.google.dev/gemma/docs/jax_inference

[^70]: https://pypi.org/project/transformers/

[^71]: https://www.youtube.com/watch?v=1RcORri2ZJg

[^72]: https://www.datacamp.com/tutorial/combine-google-gemma-with-tpus-fine-tune-and-run-inference-with-enhanced-performance-and-speed

[^73]: https://github.com/huggingface/transformers/blob/main/examples/flax/README.md

[^74]: https://www.instaclustr.com/education/top-10-open-source-llms-for-2025/

[^75]: https://github.com/AI-Hypercomputer/maxtext

[^76]: https://github.com/google/flax/discussions/2905

[^77]: https://github.com/eugeneyan/open-llms

[^78]: https://huggingface.co/docs/transformers/en/main_classes/model

[^79]: https://github.com/google/flax/issues/821

[^80]: https://flax.readthedocs.io/en/latest/guides/linen_to_nnx.html

[^81]: https://github.com/google/nerfies/issues/51

[^82]: https://github.com/google/flax/discussions/3521

[^83]: https://github.com/huggingface/notebooks/blob/master/examples/masked_language_modeling_flax.ipynb

[^84]: https://colab.research.google.com/github/phlippe/uvadlc_notebooks/blob/master/docs/tutorial_notebooks/JAX/tutorial6/Transformers_and_MHAttention.ipynb

[^85]: https://github.com/google/flax/blob/main/docs_nnx/mnist_tutorial.ipynb

[^86]: https://github.com/google/flax/discussions/927

[^87]: https://stackoverflow.com/questions/tagged/flax?tab=Active

[^88]: https://stackoverflow.com/questions/78249695/how-can-i-convert-a-flax-linen-module-to-a-torch-nn-module

