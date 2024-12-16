class Navigation {
    constructor() {
        this.menu = document.querySelector('[role="navigation"]');
        this.menuButton = this.menu.querySelector('button:first-of-type');
        this.menuButton.addEventListener('click', this.toggleMenu.bind(this));
        console.log('Navigation initialized');
    }

    toggleMenu() {
        this.menu.classList.toggle('is-open');
    }
}

new Navigation();
