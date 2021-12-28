# TLDR-IFY_API

This creates an API to do basic summarization of long text files. If you want to utilize this API feel free to check out my other projects!


## Getting Started

### Dependencies

Docker or Python3 installed. 

### Installing
#### Using Docker
1) Clone the repo
2) Inside the repo run `docker-compose up`

<i>Note: Docker will run in production by default</i>

#### Using Python
1) I recommend setting up a virtual environment
2) Install the dependencies within requirements.txt `pip install -r requirements.txt`
3) run the run.py file `python run.py`

### Executing
After running either the docker image or python file, hit the endpoint http://localhost:8080 for docker or port 5000 for locally run images. The endpoint expects a secret key for prod found in the secret.yml file generated on startup.

## Authors

Jacob Ortmann

Github - [jacobCOR](https://github.com/jacobCOR)

## License

This project is licensed under the MIT License.


