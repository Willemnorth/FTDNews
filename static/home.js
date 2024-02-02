document.addEventListener('DOMContentLoaded', () => {
    // Your other initialization code can go here

    // Function to fetch articles from Flask server
    async function fetchArticles() {
        const articlesURL = '/articles'; // Route to Flask backend

        try {
            const response = await fetch(articlesURL);
            const data = await response.json();

            // Check if response contains articles
            if (data.articles) {
                const newsContainer = document.getElementById('news-container');

                // Clear existing content
                newsContainer.innerHTML = '';

                // Loop through articles and create HTML elements
                data.articles.forEach(article => {
                    const articleDiv = document.createElement('div');
                    articleDiv.classList.add('article');

                    const articleTitle = document.createElement('h2');
                    articleTitle.textContent = article.title;

                    const articleDescription = document.createElement('p');
                    articleDescription.textContent = article.description;

                    const articleLink = document.createElement('a');
                    articleLink.href = article.url;
                    articleLink.textContent = 'Read More';

                    articleDiv.appendChild(articleTitle);
                    articleDiv.appendChild(articleDescription);
                    articleDiv.appendChild(articleLink);

                    newsContainer.appendChild(articleDiv);
                });
            }
        } catch (error) {
            console.error('Error fetching articles:', error);
        }
    }

    
});

