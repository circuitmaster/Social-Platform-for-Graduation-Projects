//modal
const signupButton = document.querySelector('#signup');
const loginButton = document.querySelector('#login');
const modalBg = document.querySelector('#mbg');
const modalBg2 = document.querySelector('#mbg2');
const modal = document.querySelector('#regmod');
const modal2 = document.querySelector('#logmod');

signupButton.addEventListener('click', () => {
	modal.classList.add('is-active');
})

modalBg.addEventListener('click', () => {
	modal.classList.remove('is-active');
})

modalBg2.addEventListener('click', () => {
	modal2.classList.remove('is-active');
})

loginButton.addEventListener('click', () => {
	modal2.classList.add('is-active');
})