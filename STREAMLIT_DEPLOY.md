Streamlit Cloud deployment steps

1) On Streamlit Cloud (https://share.streamlit.io) sign in with GitHub.
2) Click **New app → From a GitHub repo**.
   - Repository: `pythonworlddev2024-sketch/python-`
   - Branch: `main`
   - Main file: `app.py`
3) Before deploying, add the `GOOGLE_API_KEY` secret:
   - Open your app on Streamlit Cloud → **Settings** → **Secrets** → **New secret**
   - Key: `GOOGLE_API_KEY`
   - Value: (paste your key)
   - Save and click **Deploy** (or trigger a redeploy).

Notes:
- Do NOT commit real secrets to the repo. Use the Cloud Secrets UI.
- If you need a local test, create a `.streamlit/secrets.toml` file locally (do not commit):

  [google]
  api_key = "YOUR_KEY_HERE"

  And in your code read it with `st.secrets.get("google", {}).get("api_key")`.

If you want, I can watch for your confirmation after you add the secret and then verify the deployed app URL.
