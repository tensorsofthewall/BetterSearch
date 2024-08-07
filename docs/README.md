<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Meta Llama License][llama-3-shield]][llama-3-license]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/sandesh-bharadwaj/BetterSearch">
    <img src="images/logo.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">BetterSearch</h3>

  <p align="center">
    Desktop search :handshake: LLMs.
    <br />
    <br />
    <a href="https://github.com/sandesh-bharadwaj/BetterSearch/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/sandesh-bharadwaj/BetterSearch/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#compute-mode">Compute Mode</a></li>
    <li><a href="#examples">Examples</a></li>
    <li><a href="#known-issues">Known Issues</a></li>
    <li><a href="#creating-your-own-configurations">Creating your own Configurations</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![startup_screen]

**BetterSearch** is a desktop search tool that brings natural language to traditional file search. BetterSearch allows you to ask questions directly to your laptop/PC and get detailed answers, without sending your files to the cloud. Currently in its *alpha version*, **BetterSearch** is available only for *Windows* machines, with plans to support *Windows, MacOS, and Linux* in the full release.

Leveraging the powerful indexing features of existing search systems on Windows and MacOS, BetterSearch performs *on-the-fly indexing* and updates its content index automatically, even when files are added, deleted, or modified. Users do not need to manually add files for querying.

BetterSearch employs two state-of-the-art models for embedding and querying:
1. [**SQLCoder**](https://huggingface.co/defog/llama-3-sqlcoder-8b) - A fine-tuned Llama-3 model from Defog.ai, designed for SQL generation from natural language queries.
2. [**gte-v1.5**](https://huggingface.co/Alibaba-NLP/gte-base-en-v1.5) - Alibaba’s gte-v1.5 series of models, known for its advanced embeddings, extended context lengths, and efficient memory usage.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![LangChain][LangChain-shield]][Langchain-url]
* [![Transformers][Transformers-shield]][Transformers-url]
* [![OpenVINO][OpenVINO-shield]][OpenVINO-url]
* [![Optimum][Optimum-shield]][Optimum-url]
* [![Chroma][Chroma-shield]][Chroma-url]
<!-- * [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url] -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
**CAUTION: only Windows is supported currently, BetterSearch will not work on a Linux or MacOS installation.**

### Prerequisites

Ensure you have Python >= 3.9 installed, either through a local setup or virtual environment. I recommend creating a virtual environment using [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) or [venv](https://docs.python.org/3/library/venv.html).

After creating your environment, clone the repo and install the necessary dependencies:
```sh
git clone https://github.com/sandesh-bharadwaj/BetterSearch.git
cd BetterSearch

pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
To start the application, run:
```sh
python app.py
```

On the first few runs, **BetterSearch** will take time for initial indexing and downloading the necessary models (depending on internet speeds), so please be patient. You can speed up file indexing by starting the application, switching the `Compute Mode` setting to a *GPU-based* option (if you have a compatible Nvidia GPU), and then restarting the application. For more information, see [Compute Mode](#compute-mode).

Once the initial setup is complete, the application will start up *much faster* on subsequent launches.

**BetterSearch** can answer questions related to both *file properties* and *file contents*.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Compute Mode
By default, **BetterSearch** uses the *CPU-Only* setting. However, GPU options are also available, and you can create your custom configurations by modifying the respective JSON files.

1. **CPU-Only** - This setting loads both the vector embedding model and SQLCoder on the CPU, using the OpenVINO-optimized version of SQLCoder [available here](https://huggingface.co/sandeshb/SQLCoder-8b-int8-ov). This setting consumes a significant amount of memory, so expect slower responses if you don't have sufficient RAM. (Tested and verified on Intel i7-12800HX, 32GB of RAM)

2. **GPU VRAM < 10GB** - SQLCoder is loaded using *4-bit* optimization on the GPU. Requires at least **6GB of VRAM** to work correctly. (Tested and verified on Nvidia RTX 3070Ti)

3. **GPU VRAM < 16GB** - SQLCoder is loaded using *8-bit* optimization on the GPU. Requires at least **10GB of VRAM** to work correctly. (Not tested; please report any bugs)

4. **GPU VRAM > 16GB** - SQLCoder is loaded using *16-bit* optimization on the GPU. (Not tested; please report any bugs)

Additionally, you can choose to load only the vector embedding model on the GPU, while loading SQLCoder on the CPU. This can be done by setting `embd_model_device` to `cuda` instead of `cpu` in [`cpu_only.json`](../cpu_only.json). This configuration allows for fast file content indexing without requiring a powerful GPU to run SQLCoder.

<!-- USAGE EXAMPLES -->
## Examples

### Questions Using the Search Index:
1. "How many files were modified after September 10, 2021?"

2. "What are the three largest files on my system?"

![sample_query_screen]

### Questions Using the Content Index:
1. "What is the penalty for not wearing a seatbelt in a passenger vehicle in Massachusetts?" - Information available in the Massachusetts Driving Manual PDF on my local machine.

2. "Give me a brief summary of Sandesh's thesis during his MS at Boston University." - Information available in my resume. :wink:


## Known Issues
1. Llama-3 seems to be prone to strange errors and failure to follow the prompt due to quantization, and I have experienced the same when running BetterSearch in `CPU-Only` and `GPU VRAM < 10GB` modes. At the moment, there isn't a solution to this issues, but using the latter two GPU settings in `Compute Mode` should yield better results. 

2. File content queries can be bad, due to the chunk size and chunk overlap settings. This can be improved through smarter indexing, and a good reference point is [Greg Kamradt's tutorial](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb). Alternatively, this could also be due to the nature of the embedding model being used, but extensive testing is required to confirm this.

## Creating Your Own Configurations

To create your own configuration files, follow the structure provided in any of the pre-defined configuration files and adjust them as needed.

- ***"model_name"***: This specifies the LLM model used for search. I recommend:
  + *"defog/llama-3-sqlcoder-8b"* - If you have an Nvidia GPU that supports one of the available GPU configs. Intel GPUs are also supported using the [Intel Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch/tree/xpu-master).
  + *"sandeshb/llama-3-sqlcoder-8b-int8-ov"* - If you have an Intel CPU or GPU. Note that AMD CPUs may not experience the same level of speedup with OpenVINO models.
- **"cache_dir"**: The cache directory where the models are downloaded (*`"cache_dir/"`* by default).
- **"bnb_config"**: Configuration for [BitsAndBytes](https://huggingface.co/docs/bitsandbytes/main/en/index); refer to the documentation for more details.
- **"kv_cache_flag"**: Sets the `use_cache` flag for generation models in Hugging Face Transformers. It is recommended to set this to `true` always.
- **"num_beams"**: Number of beams for beam search (default=`4`).
- **"db_path"**: Location of the content index (Chroma)(*`"better_search_content_db/"`* by default).
- **"embd_model_device"**: Decides where *gte-v1.5* will be loaded. (Options: `"cpu"`, `"cuda"`)
- **"check_interval"**: Interval (in seconds) at which BetterSearch checks the filesystem for changes and updates its content index (default=`30`).
- **"chunk_size"**: Chunk size for storing vector embeddings in Chroma (default=`500`).
- **"chunk_overlap"**: Overlap between vector embedding chunks in Chroma (default=`150`). It is recommended to keep this value between `10%-20%` of **"chunk_size"**.
- **"chunk_batch_size"**: Batch size for adding embedding chunks to Chroma. This should be set based on the amount of RAM available, as setting it too high can crash the app. (Default is `500`, adjust according to your preference.)
- **"top_k"**: Number of documents retrieved based on the query in Chroma (default=`3`).

<!-- ROADMAP -->
## Roadmap

- [ ] Folder whitelists/blacklists for content indexing.
- [ ] Improve content querying through chunk size and overlap controls.
- [ ] Add more settings for controlling generation.
- [ ] Migrate from using OS-specific search indexes to custom SQL database for better SQL querying and customizability.
- [ ] Add MacOS support
- [ ] Add Linux support 


See the [open issues](https://github.com/sandesh-bharadwaj/BetterSearch/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would improve this, please **open an issue** with the tag *"enhancement"*.You can also **fork the repo** and create a pull request. Your feedback is greatly appreciated!
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE`](../LICENSE) for more information.

Llama-3 is used under the Meta Llama-3 License. See ['LLAMA-3-LICENSE'](../LLAMA-3-LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sandesh Bharadwaj - sandesh.bharadwaj97@gmail.com

Project Link: [https://github.com/sandesh-bharadwaj/BetterSearch](https://github.com/sandesh-bharadwaj/BetterSearch)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Meta for their continued contribution to open-source AI.
* Defog.ai for their fine-tuned versions of text-to-SQL models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/sandesh-bharadwaj/BetterSearch.svg?style=for-the-badge
[contributors-url]: https://github.com/sandesh-bharadwaj/BetterSearch/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sandesh-bharadwaj/BetterSearch.svg?style=for-the-badge
[forks-url]: https://github.com/sandesh-bharadwaj/BetterSearch/network/members
[stars-shield]: https://img.shields.io/github/stars/sandesh-bharadwaj/BetterSearch.svg?style=for-the-badge
[stars-url]: https://github.com/sandesh-bharadwaj/BetterSearch/stargazers
[issues-shield]: https://img.shields.io/github/issues/sandesh-bharadwaj/BetterSearch.svg?style=for-the-badge
[issues-url]: https://github.com/sandesh-bharadwaj/BetterSearch/issues
[license-shield]: https://img.shields.io/github/license/sandesh-bharadwaj/BetterSearch.svg?style=for-the-badge
[license-url]: https://github.com/sandesh-bharadwaj/BetterSearch/blob/main/LICENSE
[llama-3-shield]: https://img.shields.io/badge/License-Llama%203-purple.svg?style=for-the-badge
[llama-3-license]: https://github.com/sandesh-bharadwaj/BetterSearch/blob/main/LLAMA-3-LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/sandeshbharadwaj97
[startup_screen]: images/initial_screen.png
[sample_query_screen]: images/search_index_answer.png

[Python-url]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Langchain-shield]: https://img.shields.io/badge/LangChain-0.2.12-1C3C3C?style=for-the-badge&logo=langchain
[Langchain-url]: https://github.com/langchain-ai/langchain
[Transformers-shield]: https://img.shields.io/badge/Transformers-4.42.4-blue?style=for-the-badge
[Transformers-url]: https://github.com/huggingface/transformers
[Optimum-shield]: https://img.shields.io/badge/Optimum-1.21.2-blue?style=for-the-badge
[Optimum-url]: https://github.com/huggingface/optimum
[OpenVINO-shield]: https://img.shields.io/badge/OpenVINO-2024.3-purple?style=for-the-badge
[OpenVINO-url]: https://github.com/openvinotoolkit/openvino
[Chroma-shield]: https://img.shields.io/badge/Chroma-0.5.5-blue?style=for-the-badge
[Chroma-url]: https://github.com/chroma-core/chroma
