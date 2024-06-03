conda activate farmsafe
# resting 10 seconds to make sure the server is up
sleep 10
python main.py >> $HOME/email.txt 2>&1
