const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add('active');
});

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
});

function onLoad() {
  gapi.load('auth2', function() {
      gapi.auth2.init({
          client_id: 'YOUR_CLIENT_ID', // Replace with your Client ID
          scope: 'profile email'
      });
  });
}

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  var userId = profile.getId();
  var name = profile.getName();
  var imageUrl = profile.getImageUrl();
  var email = profile.getEmail();

  document.getElementById('user-info').innerHTML = `
      <p>User ID: ${userId}</p>
      <p>Name: ${name}</p>
      <p>Email: ${email}</p>
      <img src="${imageUrl}" alt="User Profile Image" />
  `;
}
