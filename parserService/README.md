conda create -n apiparser python=3.7.3
conda activate apiparser
pip install flask flask-jsonpify flask-sqlalchemy flask-restful
pip install requests
pip install tika==1.19
pip install numpy
pip install spacy
python -m spacy download es