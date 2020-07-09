# messenger-data-analysis

Analytics for your Facebook Messenger<sup>1</sup> data dump (quantitative metrics and textual analysis)

## Usage

> :warning: **Due to privacy concerns this program is built to be used locally on downloaded data by individuals who have claim to said data**

### Downloading Data

1. To download your Facebook Messenger data follow instructions relevant to your Facebook version [as described by the Facebook Help Center](https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav).

**Ensure you have selected the "Messages" category**

2. Clone this repository `git clone https://github.com/SirajChokshi/messenger-data-analysis.git` or download as zip.

3. Proceed to extract the `facebook-<name>.zip` folder and navigate to the contents of `messages/`. Place the contents of this folder in your clone of this repository<sup>2</sup>.

Ensure that your file structure looks something like this:

```
├── 📄 .gitignore
├── 📄 README.md
├── 📄 LICENSE
├── 📄 analyze.py
├── 📄 requirements.txt
├── 📁 inbox/
├── 📁 message_requests/
└── 📁 stickers_used/
```

### Running the program

1. Install dependencies `pip install -r requirements.txt`

2. Proceed to run the script in a Python 3 environment.

## Licensing

NCSA/University of Illinois license. Feel free to fork, remix, share, and incorporate into your own work.

## Footnotes

1. _not associated, authorized, or endorsed by Facebook. Software and related trademarks regarding Messenger are owned bt Facebook_

2. _this program only requires an `inbox/` folder to function_