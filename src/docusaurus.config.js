// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Cadre de référence — Observabilité Plateforme",
  tagline: "Standards, guides et catalogue d'assets pour l'observabilité de la plateforme",
  favicon: "img/favicon.ico",

  // URL de production du site — à adapter selon votre GitLab Pages
  url: "https://plateforme.gitlab.io",
  baseUrl: "/observabilite/",

  // GitLab Pages — configuration déploiement
  organizationName: "plateforme",
  projectName: "cadre-reference-observabilite",

  onBrokenLinks: "warn",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "fr",
    locales: ["fr"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          routeBasePath: "/",
          // Lien "Modifier cette page" vers GitLab — à adapter
          editUrl:
            "https://gitlab.com/plateforme/cadre-reference-observabilite/-/edit/main/",
          showLastUpdateTime: true,
          showLastUpdateAuthor: false,
        },
        blog: false,
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Bannière de navigation
      navbar: {
        title: "Observabilité Plateforme",
        logo: {
          alt: "Logo Plateforme",
          src: "img/logo.svg",
        },
        items: [
          {
            type: "docSidebar",
            sidebarId: "observabiliteSidebar",
            position: "left",
            label: "Documentation",
          },
          {
            href: "https://gitlab.com/plateforme/cadre-reference-observabilite",
            label: "GitLab",
            position: "right",
          },
        ],
      },

      // Pied de page
      footer: {
        style: "dark",
        links: [
          {
            title: "Sections",
            items: [
              { label: "Vision & Principes",        to: "/vision" },
              { label: "Standards & Cadre",         to: "/standards" },
              { label: "Architecture",              to: "/architecture" },
              { label: "Guides d'implémentation",   to: "/guides" },
              { label: "Prise en main",             to: "/prise-en-main" },
              { label: "Catalogue des assets",      to: "/catalogue" },
              { label: "Gouvernance",               to: "/gouvernance" },
            ],
          },
          {
            title: "Ressources externes",
            items: [
              {
                label: "Elastic Documentation",
                href: "https://www.elastic.co/guide/index.html",
              },
              {
                label: "ECS Reference",
                href: "https://www.elastic.co/guide/en/ecs/current/index.html",
              },
              {
                label: "APM Agent Java",
                href: "https://www.elastic.co/guide/en/apm/agent/java/current/index.html",
              },
              {
                label: "SRE Book — Google",
                href: "https://sre.google/sre-book/monitoring-distributed-systems/",
              },
            ],
          },
          {
            title: "Équipe plateforme",
            items: [
              {
                label: "Slack #plateforme-observabilite",
                href: "https://slack.com",
              },
              {
                label: "Jira — Projet PLAT",
                href: "https://jira.plateforme.interne",
              },
            ],
          },
        ],
        copyright: `Cadre de référence Observabilité — Équipe Plateforme — ${new Date().getFullYear()}`,
      },

      // Barre de recherche Algolia (optionnel — commenter si non utilisé)
      // algolia: {
      //   appId: 'VOTRE_APP_ID',
      //   apiKey: 'VOTRE_API_KEY',
      //   indexName: 'observabilite-plateforme',
      // },

      // Annonce en haut de page (optionnel)
      // announcementBar: {
      //   id: 'wip',
      //   content: '🚧 Ce cadre de référence est en cours de rédaction.',
      //   backgroundColor: '#fff3cd',
      //   textColor: '#856404',
      //   isCloseable: true,
      // },

      prism: {
        theme: require("prism-react-renderer").themes.github,
        darkTheme: require("prism-react-renderer").themes.dracula,
        additionalLanguages: ["java", "yaml", "xml", "bash", "json"],
      },

      colorMode: {
        defaultMode: "light",
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },

      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 3,
      },
    }),
};

module.exports = config;
