window.$docsify = {
    name: "SaleSights",
    logo: "assets/img/salesights-logo.png",
    loadSidebar: true,
    el: "#app",
    subMaxLevel: 3,
    search: "auto",
    search: {
        maxAge: 86400000,
        paths: "auto",
        placeholder: "Type to search",
        noData: "No Results!",
        depth: 6,
        hideOtherSidebarContent: true,
    },
    repo: "true",
    corner: {
        url: "https://github.com/ronan-s1/SaleSights",  
        icon: "github"
    },
    copyCode: {
        buttonText: {
            "/": "Copy"
        },
        errorText: {
            "/": "Error"
        },
        successText: {
            "/": "Copied"
        }
    }
}