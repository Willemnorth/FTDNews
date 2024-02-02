from flask import Flask, render_template, request, jsonify
from newsapi import NewsApiClient

app = Flask(__name__)

@app.route('/health')
def health_check():
    # Perform any necessary health checks here
    # For simplicity, just return 'OK' if the application is healthy
    return 'OK', 200
    
# Initialize News API client
newsapi = NewsApiClient(api_key='ec6bfaf809a74feab621d4d359f13f00')

# Function to get sources and domains
def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
        id = e['id']
        domain = e['url'].replace("http://", "").replace("https://", "").replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    sources = ", ".join(sources)
    domains = ", ".join(domains)
    return sources, domains

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        related_news = newsapi.get_everything(q=keyword,
                                              sources=sources,
                                              domains=domains,
                                              language='en',
                                              sort_by='relevancy')
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100:
            no_of_articles = 100
        all_articles = newsapi.get_everything(q=keyword,
                                              sources=sources,
                                              domains=domains,
                                              language='en',
                                              sort_by='relevancy',
                                              page_size=no_of_articles)['articles'][:5]  # Limit to top 5 articles
        return render_template("index.html", all_articles=all_articles, keyword=keyword)
    else:
        top_headlines = newsapi.get_top_headlines(country="us", language="en")
        total_results = top_headlines['totalResults']
        if total_results > 100:
            total_results = 100
        all_headlines = newsapi.get_top_headlines(country="us",
                                                   language="en",
                                                   page_size=total_results)['articles'][:5]  # Limit to top 5 articles
        return render_template("index.html", all_headlines=all_headlines)

@app.route("/search", methods=['GET'])
def search():
    category = request.args.get('category')
    sources, domains = get_sources_and_domains()
    related_articles = newsapi.get_atop_headlines(category=category,
                                                  language='en',
                                                  page_size=5)['articles']

    return jsonify(category_articles=related_articles)

if __name__ == "__main__":
    # Run the Flask app using Gunicorn
    # Use 0.0.0.0 to listen on all public IPs
    app.run(debug=True, host='0.0.0.0')
