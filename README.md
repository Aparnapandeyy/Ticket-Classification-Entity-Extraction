# 🤖 AI Internship Assignment – Vijayi WFH Technologies Pvt. Ltd

**👩‍💻 Candidate:** Aparna Pandey  
**📆 Duration:** May – June 2025  
**📂 Tasks Submitted:** ✅ Task 1 – Support Ticket Classifier 
**🎥 Video Walkthrough:** [Watch Demo Video](https://drive.google.com/drive/u/1/folders/1gSsVl_fWdiG-YFsKaqPMqclJs8ZvJX9x)  
**📓 Google Colab Notebooks:** [Open Colab Folder](https://drive.google.com/drive/u/1/folders/1gSsVl_fWdiG-YFsKaqPMqclJs8ZvJX9x)

---

## 📁 Repository Structure


---

## 🧾 Task 1 – Customer Support Ticket Classifier & Entity Extractor

### 🎯 Objective

Build a multi-task machine learning pipeline to:
- Classify support tickets into **Issue Type** and **Urgency Level**
- Extract key entities: **Product Names**, **Dates**, and **Complaint Keywords**

### 🛠️ Key Steps

- **Data Cleaning**: Lowercasing, punctuation removal, stopword removal, lemmatization
- **Feature Engineering**: 
  - TF-IDF
  - Ticket length, sentiment polarity
- **Modeling**:
  - Logistic Regression & Random Forest
  - Separate models for issue type & urgency classification
- **Entity Extraction**:
  - Rule-based (keywords, regex for dates, dictionary for products)
- **Integration**:
  - Unified function for prediction and entity extraction
- **Gradio Interface** *(optional)*

### 📊 Evaluation

- Accuracy, Precision, Recall, F1-score
- Confusion matrix & class distribution visualizations

### 🚀 Run Instructions

```bash
cd task1_ticket_classifier
jupyter notebook ticket_classifier.ipynb
# or (to launch UI)
python gradio_app.py



