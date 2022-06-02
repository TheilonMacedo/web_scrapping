mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"${cefirsussuara@gmail.com}\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml