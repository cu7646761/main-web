
// let thumbnail = 'https://storage.googleapis.com/hackersandslackers-cdn/2019/10/pandas-difference.jpg'
// let title = 'Comparing Rows Between Two Pandas DataFrames'
// let description = 'Find which rows are different between two DataFrames, as well as which DataFrame they are unique to.'
// let createdAt = 'No no'






let BLOG_HOST = "https://original-glider-246113.appspot.com/posts?slug="
let POST_API = 'https://original-glider-246113.appspot.com/posts'
// fetch(POST_API).then(response => {
//   return response.json();
// }).then(data => {
//   let posts = data.data;
//   postFeed = document.getElementsByClassName("post-feed")[0]
//   showPosts(posts, postFeed);

//   postFeed = document.getElementsByClassName("post-feed")[0]
//   return addPagination(data.current_page, data.total_pages, postFeed)
// }).then(pageInfo => {
//   console.log(pageInfo)


// }).catch(function (e) {
//   console.log("Booo", e);
// });
async function start() {
  let response = await fetch(POST_API);
  postsInfo = await response.json()

  let postFeed = document.getElementsByClassName("post-feed")[0]

  await showPosts(postsInfo.data, postFeed)
  await addPagination(postsInfo.current_page, postsInfo.total_pages, postFeed)
  console.log(postsInfo)
}


start()

let addPagination = (currentPage, totalPages, postFeed) => {
  let perviousVisibility = currentPage == 1 ? "hidden" : "visible";
  let nextVisibility = currentPage == totalPages ? "hidden" : "visible";


  document.getElementById("current-page-of-pages").innerText = "Page " + currentPage + " of " + totalPages

  document.getElementById("a-tag-previous-post").style.visibility = perviousVisibility
  document.getElementById("a-tag-next-post").style.visibility = nextVisibility
  // postFeed.insertAdjacentHTML('beforeend', paginationSection);

  return [currentPage, totalPages]

}




let showPosts = (posts, postFeed) => {
  for (let pi = posts.length - 1; pi >= 0; pi--) {
    const post = posts[pi];

    let title = post.title;
    let description = "Find which rows are different between two DataFrames, as well as which DataFrame they are unique to.";
    let createdAt = "No no"
    let thumbnail = post.thumbnail;
    let slug = post.slug;

    var baseCard = `
<div class="post-card"><a
href="/blog-post/${slug}"><img
  class="post-card-image lazyloaded"
  alt="Comparing Rows Between Two Pandas DataFrames" src="${thumbnail}"></a>
<div class="post-card-detail"><a
  href="/blog-post/${slug}">
  <h2 class="post-card-title">${title}</h2>
</a>
<section class="post-card-excerpt">${description}</section>
<footer class="post-card-footer">
  <div class="meta-item tag"><svg aria-hidden="true" focusable="false" data-prefix="far"
      data-icon="tag" class="svg-inline--fa fa-tag fa-w-16 fa-sm " role="img"
      xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
      <path fill="currentColor"
        d="M497.941 225.941L286.059 14.059A48 48 0 0 0 252.118 0H48C21.49 0 0 21.49 0 48v204.118a47.998 47.998 0 0 0 14.059 33.941l211.882 211.882c18.745 18.745 49.137 18.746 67.882 0l204.118-204.118c18.745-18.745 18.745-49.137 0-67.882zM259.886 463.996L48 252.118V48h204.118L464 259.882 259.886 463.996zM192 144c0 26.51-21.49 48-48 48s-48-21.49-48-48 21.49-48 48-48 48 21.49 48 48z">
      </path>
    </svg><span class="Ghost__Post__5d9e7c2eeb21dc3332d4054f">Pandas</span></div>
  <div class="meta-item reading-item"> <svg aria-hidden="true" focusable="false" data-prefix="far"
      data-icon="eye" class="svg-inline--fa fa-eye fa-w-18 fa-sm " role="img"
      xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512">
      <path fill="currentColor"
        d="M288 144a110.94 110.94 0 0 0-31.24 5 55.4 55.4 0 0 1 7.24 27 56 56 0 0 1-56 56 55.4 55.4 0 0 1-27-7.24A111.71 111.71 0 1 0 288 144zm284.52 97.4C518.29 135.59 410.93 64 288 64S57.68 135.64 3.48 241.41a32.35 32.35 0 0 0 0 29.19C57.71 376.41 165.07 448 288 448s230.32-71.64 284.52-177.41a32.35 32.35 0 0 0 0-29.19zM288 400c-98.65 0-189.09-55-237.93-144C98.91 167 189.34 112 288 112s189.09 55 237.93 144C477.1 345 386.66 400 288 400z">
      </path>
    </svg> <span>5 min read</span> </div>
  <div class="meta-item author"><svg
        aria-hidden="true" focusable="false" data-prefix="far" data-icon="user-edit"
        class="svg-inline--fa fa-user-edit fa-w-20 fa-sm " role="img"
        xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512">
        <path fill="currentColor"
          d="M358.9 433.3l-6.8 61c-1.1 10.2 7.5 18.8 17.6 17.6l60.9-6.8 137.9-137.9-71.7-71.7-137.9 137.8zM633 268.9L595.1 231c-9.3-9.3-24.5-9.3-33.8 0l-41.8 41.8 71.8 71.7 41.8-41.8c9.2-9.3 9.2-24.4-.1-33.8zM223.9 288c79.6.1 144.2-64.5 144.1-144.1C367.9 65.6 302.4.1 224.1 0 144.5-.1 79.9 64.5 80 144.1c.1 78.3 65.6 143.8 143.9 143.9zm-4.4-239.9c56.5-2.6 103 43.9 100.4 100.4-2.3 49.2-42.1 89.1-91.4 91.4-56.5 2.6-103-43.9-100.4-100.4 2.3-49.3 42.2-89.1 91.4-91.4zM134.4 352c14.6 0 38.3 16 89.6 16 51.7 0 74.9-16 89.6-16 16.7 0 32.2 5 45.5 13.3l34.4-34.4c-22.4-16.7-49.8-26.9-79.9-26.9-28.7 0-42.5 16-89.6 16-47.1 0-60.8-16-89.6-16C60.2 304 0 364.2 0 438.4V464c0 26.5 21.5 48 48 48h258.3c-3.8-14.6-2.2-20.3.9-48H48v-25.6c0-47.6 38.8-86.4 86.4-86.4z">
        </path>
      </svg><span>Admin</span> </a></div>
  <div class="meta-item date"> <svg aria-hidden="true" focusable="false" data-prefix="far"
      data-icon="calendar" class="svg-inline--fa fa-calendar fa-w-14 fa-sm " role="img"
      xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
      <path fill="currentColor"
        d="M400 64h-48V12c0-6.6-5.4-12-12-12h-40c-6.6 0-12 5.4-12 12v52H160V12c0-6.6-5.4-12-12-12h-40c-6.6 0-12 5.4-12 12v52H48C21.5 64 0 85.5 0 112v352c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V112c0-26.5-21.5-48-48-48zm-6 400H54c-3.3 0-6-2.7-6-6V160h352v298c0 3.3-2.7 6-6 6z">
      </path>
    </svg> <span>${createdAt}</span> </div>
</footer>
</div>
</div>
`

    postFeed.insertAdjacentHTML('afterbegin', baseCard);
  }
}

let nextPageTag = document.getElementById("a-tag-next-post");


nextPageTag.addEventListener("click", event => {
  event.preventDefault();

  let pageLocation = document.getElementById("current-page-of-pages").innerText.split(" ");

  currentPage = pageLocation[1];
  TotalPages = pageLocation[3];

  let nextPageNumber = 1 + + currentPage;

  fetch(POST_API + "?page=" + nextPageNumber).then(response => {
    return response.json();
  }).then(data => {
    let posts = data.data;
    postFeed = document.getElementsByClassName("post-feed")[0]

    removePostFeed()
    removePostFeed()
    removePostFeed()
    removePostFeed()


    showPosts(posts, postFeed);

    scrollToTop();
    return addPagination(data.current_page, data.total_pages, postFeed)
  })
})

let previousPageTag = document.getElementById("a-tag-previous-post");


previousPageTag.addEventListener("click", event => {
  event.preventDefault();

  let pageLocation = document.getElementById("current-page-of-pages").innerText.split(" ");

  currentPage = pageLocation[1];
  TotalPages = pageLocation[3];

  let previousPageNumber = +currentPage - 1;

  fetch(POST_API + "?page=" + previousPageNumber).then(response => {
    return response.json();
  }).then(data => {
    let posts = data.data;
    let postFeed = document.getElementsByClassName("post-feed")[0]

    removePostFeed()
    removePostFeed()
    removePostFeed()
    removePostFeed()


    showPosts(posts, postFeed);

    scrollToTop();
    return addPagination(data.current_page, data.total_pages, postFeed)
  })
})

const scrollToTop = () => {
  const c = document.documentElement.scrollTop || document.body.scrollTop;
  if (c > 0) {
    window.requestAnimationFrame(scrollToTop);
    window.scrollTo(0, c - c / 4);
  }
};

let removePostFeed = () => {
  let postFeed = document.getElementsByClassName("post-feed")[0]

  let listPostCards = postFeed.getElementsByClassName("post-card")

  for (let pi = 0; pi < listPostCards.length; pi++) {
    listPostCards[pi].remove();
  }
}