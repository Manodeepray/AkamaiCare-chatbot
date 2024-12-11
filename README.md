# AkamaiCare

## lokahi hackathon solution

[chatbot streamlit demo](https://akamai-care.streamlit.app/)

AkamaiCare is a powerful **chatbot-dashboard hybrid application** designed to assist hospital staff and administrators in accessing patient and hospital databases efficiently. Built using cutting-edge tools like **LlamaIndex**, **QueryAgent**, and **RetrievalAgent**, the app provides an intuitive interface for querying healthcare data, enabling streamlined operations and informed decision-making.

![AkamaiCare Logo](https://path-to-logo.com/logo.png)

## Features

- **Comprehensive Querying**: Access and retrieve data about patients, services, claims, and providers from hospital databases and PDFs.
- **Hybrid Chatbot and Dashboard**: Combines a conversational AI for intuitive querying with a dashboard for visual data representation.
- **Streamlit UI**: Clean and responsive interface deployed on Hugging Face Spaces.
- **Secure Data Access**: Ensures data integrity and compliance with healthcare standards.

## Tech Stack

- **Backend**:
  - [LlamaIndex](https://www.llamaindex.ai): Framework for efficient querying of large datasets.
  - QueryAgent & RetrievalAgent: Facilitates intelligent search and retrieval.
- **Frontend**:
  - [Streamlit](https://streamlit.io): For a lightweight, interactive web UI.
  - Hosted on [Hugging Face Spaces](https://huggingface.co/spaces): [AkamaiCare API url](https://oreonmayo-akamaicare.hf.space/chatbot/).
- **Deployment**:
  - Hugging Face Spaces for easy accessibility.

## How It Works

1. **Upload Data**: Hospital staff can upload CSV files or PDFs containing patient and hospital information.
2. **Query the Database**: Use the chatbot to ask natural language questions like:
   - _"How many patients were admitted in the last month?"_
   - _"What are the claims processed by XYZ insurance?"_
3. **Visualize Data**: View detailed reports and visualizations on the dashboard for deeper insights.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Streamlit
- Hugging Face account

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/akamai-care.git
   cd akamai-care
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application locally:
   ```bash
   streamlit run app.py
   ```
4. Deploy to Hugging Face Spaces:
   - Follow the [Hugging Face deployment guide](https://huggingface.co/docs).

## Usage

- Navigate to the [AkamaiCare App](https://oreonmayo-akamaicare.hf.space/chatbot/).
- Interact with the chatbot to query data or explore insights via the dashboard.

## Screenshots

### Chatbot Interface

![Chatbot Interface](https://path-to-screenshot.com/chatbot.png)

### Dashboard

![Dashboard](https://path-to-screenshot.com/dashboard.png)

## Contribution Guidelines

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Commit your changes and create a pull request.

## License

This project is licensed under the CC License

## Support

For issues, please open an issue on the [GitHub repository](https://github.com/yourusername/akamai-care/issues) or contact the maintainer.

---

### Acknowledgments

- The [LlamaIndex](https://www.llamaindex.ai) team for the powerful querying tools.
- The [Streamlit](https://streamlit.io) community for the flexible UI framework.
- Hugging Face Spaces for deployment support.

---

Designed with care for Hawaiian healthcare systems — AkamaiCare empowers healthcare professionals to make smarter decisions faster.

---

title: AkamaiCare
emoji: ⚡
colorFrom: yellow
colorTo: yellow
sdk: docker
pinned: false
license: cc
short_description: "lokahi hackathon solution - chatbot/dashboard for staff "

---
