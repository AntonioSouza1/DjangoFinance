// Adiciona um listener para quando a impressão terminar
window.addEventListener("afterprint", (event) => {
    window.close();
});

// Inicia a impressão assim que a página carregar
window.onload = (event) => {
    window.print();
};