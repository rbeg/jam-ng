// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  observabiliteSidebar: [
    {
      type: "doc",
      id: "vision/vision",
      label: "🏠 Accueil",
    },

    // ─────────────────────────────────────────────
    // 01 — VISION & PRINCIPES
    // ─────────────────────────────────────────────
    {
      type: "category",
      label: "🎯 Vision & Principes",
      collapsible: true,
      collapsed: false,
      link: {
        type: "doc",
        id: "vision/vision",
      },
      items: [
        "vision/01-pourquoi-observabilite",
        "vision/02-trois-piliers",
        "vision/03-principes-directeurs",
        "vision/04-observabilite-by-design",
        "vision/05-ecosysteme",
        "vision/06-golden-signals",
        "vision/07-indicateurs-metier",
        "vision/08-glossaire",
      ],
    },

    // ─────────────────────────────────────────────
    // 02 — STANDARDS & CADRE
    // ─────────────────────────────────────────────
    {
      type: "category",
      label: "📐 Standards & Cadre",
      collapsible: true,
      collapsed: true,
      link: {
        type: "doc",
        id: "standards/standards",
      },
      items: [
        {
          type: "doc",
          id: "standards/01-logs-ecs",
          label: "⛔ Logs — Format ECS",
        },
        {
          type: "doc",
          id: "standards/02-apm",
          label: "⛔ APM — Agent",
        },
        {
          type: "doc",
          id: "standards/03-labels-metier",
          label: "✅ Labels métier",
        },
        {
          type: "doc",
          id: "standards/04-alerting",
          label: "Alerting",
        },
        {
          type: "doc",
          id: "standards/05-dashboards",
          label: "Dashboards",
        },
      ],
    },

    // ─────────────────────────────────────────────
    // 03 — ARCHITECTURE
    // ─────────────────────────────────────────────
    {
      type: "category",
      label: "🏗️ Architecture",
      collapsible: true,
      collapsed: true,
      link: {
        type: "doc",
        id: "architecture/architecture",
      },
      items: [
        "architecture/01-pipeline-logs",
        "architecture/02-pipeline-apm",
        "architecture/03-pipeline-metier",
        "architecture/04-index-et-data-views",
        "architecture/05-correlation",
      ],
    },

    // ─────────────────────────────────────────────
    // 04 — GUIDES D'IMPLÉMENTATION
    // ─────────────────────────────────────────────
    {
      type: "category",
      label: "🚀 Guides d'implémentation",
      collapsible: true,
      collapsed: true,
      link: {
        type: "doc",
        id: "guides/guides",
      },
      items: [
        {
          type: "doc",
          id: "guides/01-onboarding",
          label: "✅ Checklist onboarding",
        },
        "guides/02-configurer-ecs",
        "guides/03-configurer-apm",
        "guides/04-ajouter-labels-metier",
        "guides/05-verifier-instrumentation",
      ],
    },

    // ─────────────────────────────────────────────
    // 05 — PRISE EN MAIN
    // ─────────────────────────────────────────────
    {
      type: "category",
      label: "🛠️ Prise en main",
      collapsible: true,
      collapsed: true,
      link: {
        type: "doc",
        id: "prise-en-main/prise-en-main",
      },
      items: [
        "prise-en-main/01-kibana-discover",
        {
          type: "category",
          label: "Kibana › APM",
          collapsible: true,
          collapsed: false,
          link: {
            type: "doc",
            id: "prise-en-main/02-kibana-apm/kibana-apm",
          },
          items: [
            "prise-en-main/02-kibana-apm/01-modele-de-donnees",
            "prise-en-main/02-kibana-apm/02-lire-une-trace",
            "prise-en-main/02-kibana-apm/03-analyser-transactions",
            "prise-en-main/02-kibana-apm/04-ressources",
          ],
        },
        "prise-en-main/03-kibana-dashboards",
        "prise-en-main/04-kibana-alerting",
        {
          type: "doc",
          id: "prise-en-main/05-recettes",
          label: "⚡ Recettes du quotidien",
        },
      ],
    },

    // ─────────────────────────────────────────────
    // 06 — CATALOGUE DES ASSETS
    // ─────────────────────────────────────────────
    {
      type: "category",
      label: "📦 Catalogue des assets",
      collapsible: true,
      collapsed: true,
      link: {
        type: "doc",
        id: "catalogue/catalogue",
      },
      items: [
        "catalogue/01-gouvernance-dashboards",
        {
          type: "category",
          label: "Dashboards socles",
          collapsible: true,
          collapsed: false,
          link: {
            type: "doc",
            id: "catalogue/02-dashboards-socles/dashboards-socles",
          },
          items: [
            "catalogue/02-dashboards-socles/apm-overview",
            "catalogue/02-dashboards-socles/logs-applicatifs",
            "catalogue/02-dashboards-socles/erreurs-exceptions",
          ],
        },
        {
          type: "category",
          label: "Dashboards technologiques",
          collapsible: true,
          collapsed: false,
          link: {
            type: "doc",
            id: "catalogue/03-dashboards-technologiques/dashboards-technologiques",
          },
          items: [
            "catalogue/03-dashboards-technologiques/kafka-connectors",
          ],
        },
        {
          type: "category",
          label: "Template domaine (niveau 3)",
          collapsible: true,
          collapsed: false,
          items: [
            "catalogue/04-template-domaine/guide-construction",
            "catalogue/04-template-domaine/conventions-nommage",
            "catalogue/04-template-domaine/checklist-mise-en-prod",
          ],
        },
        {
          type: "category",
          label: "Alertes socles",
          collapsible: true,
          collapsed: false,
          items: [
            "catalogue/05-alertes-socles/catalogue-alertes",
          ],
        },
      ],
    },

    // ─────────────────────────────────────────────
    // 07 — GOUVERNANCE
    // ─────────────────────────────────────────────
    {
      type: "category",
      label: "🏛️ Gouvernance",
      collapsible: true,
      collapsed: true,
      link: {
        type: "doc",
        id: "gouvernance/gouvernance",
      },
      items: [
        "gouvernance/01-equipe-plateforme",
        "gouvernance/02-contribuer",
        "gouvernance/03-demandes",
        "gouvernance/04-cycle-de-vie-assets",
      ],
    },
  ],
};

module.exports = sidebars;
