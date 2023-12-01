# Time Served
42 log time counter.

Currently only counts log time for the current week.

## Set-Up
You need to have python and requests installed

```bash
pip install requests
```

Register a new application in your intra [here](https://profile.intra.42.fr/oauth/applications), then provide the credentials from environment variables.

```
export FT_UID=<api-uid>
export FT_SECRET=<api-secret>

# optional
export FT_USER=<intra-name>
```

## Usage
```bash
python3 time.py

# alternatively
python3 time.py <intra-name>
```
