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
const mobileBtn = document.getElementById("btn_mobile")
const navLinks = document.getElementById("nav_links")
const icon = document.getElementById("icon_mobile")

mobileBtn.addEventListener('click', () => {
    navLinks.classList.toggle('show_mobile')
    icon.classList.toggle('fa-times')
    icon.classList.toggle('fa-bars')
});


function toggleTransaction() {
    // Pega o elemento do menu pelo seu ID
    document.getElementById("transactionDropdown").classList.toggle("show");
}

function toggleUser() {
    // Pega o elemento do menu pelo seu ID
    document.getElementById("userDropdown").classList.toggle("show");
}

function toggleSubscription() {
    document.getElementById("subscriptionDropdown").classList.toggle("show");
}

// Opcional: Fechar o menu se o usuário clicar fora dele
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}


//dark mode
document.addEventListener('DOMContentLoaded', () => {
    const rootElement = document.documentElement; // Seleciona a tag <html>
    const toggleButton = document.getElementById('theme-toggle');
    const storageKey = 'user-theme'; // Chave para salvar a preferência

    // Função para aplicar o tema no HTML e salvar no localStorage
    const applyTheme = (theme) => {
        // Altera o atributo data-theme
        rootElement.setAttribute('data-theme', theme);

        // Salva a preferência
        localStorage.setItem(storageKey, theme);

        // Atualiza o texto do botão
        updateButtonText(theme);
    };

    // Função para alternar entre 'light' e 'dark'
    const toggleTheme = () => {
        const currentTheme = rootElement.getAttribute('data-theme');
        // Se o tema atual for 'light', muda para 'dark', senão, muda para 'light'
        const newTheme = (currentTheme === 'light' || !currentTheme) ? 'dark' : 'light';
        applyTheme(newTheme);
    };

    // Função para atualizar o texto do botão (Melhora a UX)
    const updateButtonText = (theme) => {
        if (theme === 'dark') {
            toggleButton.textContent = 'Alternar para o Modo Claro';
        } else {
            toggleButton.textContent = 'Alternar para o Modo Escuro';
        }
    };

    // --- Lógica Principal ---

    // 1. Tenta carregar a preferência do usuário salva
    const savedTheme = localStorage.getItem(storageKey);

    if (savedTheme) {
        // Se houver uma preferência salva, aplica-a
        applyTheme(savedTheme);
    } else {
        // Se não houver preferência salva, verifica o sistema do usuário (Melhor Prática)
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const initialTheme = systemPrefersDark ? 'dark' : 'light';

        // Aplica o tema inicial e salva para uso futuro
        applyTheme(initialTheme);
    }

    // 2. Adiciona o evento de clique ao botão
    toggleButton.addEventListener('click', toggleTheme);
});

document.body.addEventListener('htmx:beforeRequest', (e) => {
    // Busca o botão dentro do formulário que disparou o evento e o desabilita
    const button = e.detail.elt.querySelector('button[type="submit"]');
    if (button) button.disabled = true;
});

document.body.addEventListener('htmx:afterRequest', (e) => {
    // Reabilita após a resposta (seja sucesso ou erro)
    const button = e.detail.elt.querySelector('button[type="submit"]');
    if (button) button.disabled = false;
});

