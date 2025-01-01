# wpgen_manual

A tool for processing waypoints using a manual input approach. This README explains how to set up the environment and run the script successfully.

---

## Prerequisites

Before you begin, ensure you have the following:
- **Python 3.7**
- **conda** (or another environment manager)

---

## Installation

Follow these steps to set up the environment and install the required dependencies.

### 1. Clone the Repository
```bash
git clone https://github.com/jinkimh/wpgen_manual.git
cd wpgen_manual/
```

### 2. Create and Activate a Conda Environment
```bash
conda create -n wpgen python=3.7 -y
conda activate wpgen
```

### 3. Install Dependencies
Create a `requirements.txt` file and install the necessary Python packages:
```bash
# Create the requirements.txt file
echo "numpy
matplotlib
opencv-python
PyYAML
scipy" > requirements.txt

# Install all required packages
pip install -r requirements.txt
```

---

## Usage

To run the script, use the following command:
```bash
python3 wpgen_manual.py ./map/ict_3rd_floor.png
```

Replace `./map/ict_3rd_floor.png` with the path to your map image.

---

## Troubleshooting

### Missing Dependencies
If you encounter a `ModuleNotFoundError`, ensure all dependencies are installed correctly:
```bash
pip install -r requirements.txt
```

### Conda Environment Issues
Make sure the conda environment is activated before running the script:
```bash
conda activate wpgen
```

---

## Notes

- The environment uses Python 3.7 for compatibility.
- For additional customization or enhancements, modify the `wpgen_manual.py` script as needed.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

Happy waypoint generation!
```
