//mostrar  pagina selecionada na barra de naveçação
document.addEventListener("DOMContentLoaded", function () {
const currentURL = window.location.pathname;

const sidebarLinks = document.querySelectorAll(" #nav-links a");

sidebarLinks.forEach(link => {
  const linkURL = link.getAttribute("href");

  if (currentURL.startsWith(linkURL)) {
    link.parentElement.classList.add("active");
  }
});
});

//Alterar entre tabelas
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
button.addEventListener('click', () => {
  // Remove classe "active" de todos os botões e conteúdos
  tabButtons.forEach(btn => btn.classList.remove('active'));
  tabContents.forEach(tab => tab.classList.remove('active'));

  // Adiciona "active" à aba clicada
  button.classList.add('active');
  const tabId = button.getAttribute('data-tab');
  document.getElementById(tabId).classList.add('active');
});
});

// Remove automaticamente mensagens após 3s com animação
setTimeout(function() {
document.querySelectorAll('#messages-container .message').forEach(msg => {
  msg.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  msg.style.opacity = '0';
  msg.style.transform = 'translateX(30px)';
  setTimeout(() => msg.remove(), 600);
});
}, 3000);

//botão mobile
const mobileBtn = document.querySelector('.btn-mobile');
const navLinks = document.getElementById('nav-links');
const icon = document.querySelector('.btn-mobile i');

mobileBtn.addEventListener('click', () => {
    navLinks.classList.toggle('show')
    icon.classList.toggle('fa-times')
    icon.classList.toggle('fa-bars')
});


