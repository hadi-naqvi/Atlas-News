var panZoomMap = svgPanZoom('#svg-map');

function Article(imgSrc, title, author, url, id) {
    return {
        imgSrc: imgSrc,
        title: title,
        author: author,
        url: url,
        id: id,
        renderDiv() {
            return `
            <div id="${this.id}" class="article" onclick="openArticle(${id})">
                <img src="${this.imgSrc}" alt="">
                <p>"${this.title}</p>
                <center><p><em>${this.author}</em></p></center>
            </div>`;
        },
    };
}

function openPanel() {
    document.getElementById("sidepanel").style.width = "30%";
    document.getElementById("country-panel").style.width = "0";
    // document.getElementById("all-news").innerHTML = "";
}

function closePanel() {
    document.getElementById("sidepanel").style.width = "0";
}

function openCountryPanel(country) {
    document.getElementById("country-panel").style.width = "30%";
    document.getElementById("sidepanel").style.width = "0";
    document.getElementById("country-header").innerHTML = `Latest News in ${country}`;
    document.getElementById("country-news").innerHTML = '';

    fetch(`/country/${country}`).then(response => {console.log(response); return response.json();}).then(result => {
        for (let i = 0; i < result.length; i ++) {
            document.getElementById("country-news").innerHTML += Article(result[i].urlToImage, result[i].title, result[i].source.name, result[i].url, result[i].id).renderDiv()
        }
    })
}

function searchArticles() {
    document.getElementById("all-news").innerHTML = '';
    let query = document.getElementById("search").value;
    console.log(query)
    fetch(`/search/${query}`).then(response => {console.log(response); return response.json();}).then(result => {
        for(let i = 0; i < result.length; i++){
            console.log(result[i]);
            console.log(result[i].id);
            document.getElementById("all-news").innerHTML += Article(result[i].urlToImage, result[i].title, result[i].source.name, result[i].url, result[i].id).renderDiv()
        }
    })
}

function closeCountryPanel() {
    document.getElementById("country-panel").style.width = "0";
}

function openArticle(articleID) {
    document.getElementById("comments").style.width = "50%";
    document.getElementById("comments-section").innerHTML = "";

    fetch(`/getarticle/${articleID}`).then(response => {console.log(response); return response.json();}).then(result => {
        console.log(result);
        document.getElementById("article-image").src = result[0].image_url;
        document.getElementById("article-title").href = result[0].url;
        document.getElementById("article-title").innerHTML = `<h1>${result[0].title}</h1>`;
        document.getElementById("date-published").innerHTML = `Published: ${result[0].date}`
        document.getElementById("like-button").href = `javascript:likePost(${articleID})`;
        document.getElementById("dislike-button").href = `javascript:dislikePost(${articleID})`;
        document.getElementById("total-likes").innerHTML = `${result[0].likes} Likes`
        document.getElementById("article-id").value = `${articleID}`;

        fetch(`/getcomments/${articleID}`).then(response2 => {console.log(response2); return response2.json()}).then(result2 => {
            console.log(result2);
            for (let i = 0; i < result2.length; i++) {
                fetch(`/getuser/${result2[i].user_id}`).then(response3 => {return response3.json()}).then(result3 => {
                    document.getElementById("comments-section").innerHTML += `<div class="user-comment" style="width: 300px; height: 100px;"><h2>${result3[0].first_name}</h2><p>${result2[i].comment}</p><p><em>Posted: ${result2[i].date}</em></p></div>`;
                })
            }
        })
    })
}

function likePost(articleID) {
    fetch(`/likearticle/${articleID}`).then(response => { console.log(response); return response.json();}).then(result => {
        fetch(`/getarticle/${articleID}`).then(response2 => {console.log(response2); return response2.json();}).then(result2 => {
            document.getElementById("total-likes").innerHTML = `${result2[0].likes} Likes`;
        })
    })
}

function dislikePost(articleID) {
    fetch(`/dislikearticle/${articleID}`).then(response => { console.log(response); return response.json();}).then(result => {
        fetch(`/getarticle/${articleID}`).then(response2 => {console.log(response2); return response2.json();}).then(result2 => {
            document.getElementById("total-likes").innerHTML = `${result2[0].likes} Likes`;
        })
    })
}

function closeArticle() {
    document.getElementById("comments").style.width = "0";
}

function submitComment() {
    openArticle(document.getElementById("article-id").value);
}

function resetMap() {
    panZoomMap.resetZoom();
    panZoomMap.resetPan();
}