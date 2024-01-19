const blogPathRegex = new RegExp("/blog$");
const createBlogPostPathRegex = new RegExp("/create-blog-post$");
const loginPathRegex = new RegExp("/login$");
const signupPathRegex = new RegExp("/signup$");

window.onload = function () {
  const location = window.location.href;
  const bloggersAnchor = document.querySelector("#bloggers .link-item");
  const blogAnchor = document.querySelector("#blog .link-item");
  const createBlogPostAnchor = document.querySelector(
    "#create-blog-post .link-item"
  );
  const loginAnchor = document.querySelector("#login .link-item");

  if (blogPathRegex.test(location)) {
    blogAnchor.classList.add("selected");
  } else if (createBlogPostPathRegex.test(location)) {
    createBlogPostAnchor.classList.add("selected");
  } else if (loginPathRegex.test(location)) {
    loginAnchor.classList.add("selected");
  } else if (signupPathRegex.test(location) || location.includes("blog")) {
    // do nothing
  } else {
    bloggersAnchor.classList.add("selected");
  }
};
