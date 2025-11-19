"""seed tech tags

Revision ID: 67a6d16d7bee
Revises: 94f2f478bab5
Create Date: 2025-11-18 19:51:21.599433

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from domain.common import TechTagKind


# revision identifiers, used by Alembic.
revision: str = '67a6d16d7bee'
down_revision: Union[str, Sequence[str], None] = '94f2f478bab5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_tech_tags_seed() -> list[dict]:
    """Return initial tech tags seed."""
    return [
        # Languages
        {
            "id": uuid4(),
            "slug": "python",
            "name": "Python",
            "description": "General-purpose programming language, great for backend, data and scripting.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "javascript",
            "name": "JavaScript",
            "description": "Language for web development, runs in browsers and on Node.js.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "typescript",
            "name": "TypeScript",
            "description": "JavaScript with static typing, widely used for frontend and backend.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "go",
            "name": "Go",
            "description": "Compiled language from Google, good for high-performance services.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "java",
            "name": "Java",
            "description": "Popular language for enterprise backend and Android development.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "kotlin",
            "name": "Kotlin",
            "description": "Modern language for JVM and Android, interoperable with Java.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "csharp",
            "name": "C#",
            "description": "Language for .NET platform, backend, desktop and game development.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "rust",
            "name": "Rust",
            "description": "Systems programming language focused on safety and performance.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "ruby",
            "name": "Ruby",
            "description": "Dynamic programming language, popular for web development with Rails.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "php",
            "name": "PHP",
            "description": "Scripting language widely used for server-side web development.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "c",
            "name": "C",
            "description": "Low-level systems programming language with manual memory management.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "cpp",
            "name": "C++",
            "description": "General-purpose language with object-oriented and generic programming features.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "swift",
            "name": "Swift",
            "description": "Language for iOS, macOS and server-side applications.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "objective-c",
            "name": "Objective-C",
            "description": "Objective-oriented language for Cocoa and iOS development.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "r-lang",
            "name": "R",
            "description": "Language and environment for statistical computing and graphics.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "dart",
            "name": "Dart",
            "description": "Language optimized for client apps on mobile, web and desktop.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "scala",
            "name": "Scala",
            "description": "JVM language combining object-oriented and functional programming.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "elixir",
            "name": "Elixir",
            "description": "Functional, concurrent language built on top of the Erlang VM.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "haskell",
            "name": "Haskell",
            "description": "Purely functional programming language with strong static typing.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "clojure",
            "name": "Clojure",
            "description": "Functional Lisp dialect for the JVM.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "shell",
            "name": "Shell",
            "description": "Shell scripting languages such as Bash and Zsh.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "sql",
            "name": "SQL",
            "description": "Structured Query Language for working with relational databases.",
            "kind": TechTagKind.LANGUAGE.name,
        },
        {
            "id": uuid4(),
            "slug": "perl",
            "name": "Perl",
            "description": "High-level, general-purpose, interpreted language.",
            "kind": TechTagKind.LANGUAGE.name,
        },

        # Frameworks / libraries
        {
            "id": uuid4(),
            "slug": "django",
            "name": "Django",
            "description": "High-level Python web framework with batteries included.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "fastapi",
            "name": "FastAPI",
            "description": "Modern, fast Python web framework for building APIs.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "flask",
            "name": "Flask",
            "description": "Lightweight Python microframework for web applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "react",
            "name": "React",
            "description": "JavaScript library for building user interfaces.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "vue",
            "name": "Vue.js",
            "description": "Progressive JavaScript framework for building UIs.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "angular",
            "name": "Angular",
            "description": "Full-featured TypeScript framework for building web applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "nextjs",
            "name": "Next.js",
            "description": "React framework for server-side rendering and static sites.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "nuxt",
            "name": "Nuxt.js",
            "description": "Vue framework for server-side rendering and static sites.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "nestjs",
            "name": "NestJS",
            "description": "Progressive Node.js framework for building efficient server-side applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "spring",
            "name": "Spring",
            "description": "Java framework for building production-grade backend services.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "dotnet",
            "name": ".NET",
            "description": "Microsoft framework for building cross‑platform applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "rails",
            "name": "Ruby on Rails",
            "description": "Full-stack web framework for Ruby.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "laravel",
            "name": "Laravel",
            "description": "PHP web framework with expressive, elegant syntax.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "symfony",
            "name": "Symfony",
            "description": "Reusable PHP components and full-stack web framework.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "express",
            "name": "Express",
            "description": "Minimal and flexible Node.js web framework.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "koa",
            "name": "Koa",
            "description": "Lightweight and expressive Node.js web framework.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "sails",
            "name": "Sails.js",
            "description": "MVC framework for Node.js for data-driven APIs and apps.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "phoenix",
            "name": "Phoenix",
            "description": "Web framework for Elixir for high-performance applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "play-framework",
            "name": "Play Framework",
            "description": "Reactive web framework for Java and Scala.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "spring-boot",
            "name": "Spring Boot",
            "description": "Opinionated Spring framework for creating standalone applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "aspnet-core",
            "name": "ASP.NET Core",
            "description": "Cross-platform, high-performance framework for .NET web apps.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "flutter",
            "name": "Flutter",
            "description": "UI toolkit for building natively compiled applications from a single codebase.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "react-native",
            "name": "React Native",
            "description": "Framework for building native apps using React.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "expo",
            "name": "Expo",
            "description": "Toolchain and framework for React Native apps.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "svelte",
            "name": "Svelte",
            "description": "Compiler-based framework for building reactive user interfaces.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "sveltekit",
            "name": "SvelteKit",
            "description": "Application framework for building Svelte apps.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "ember",
            "name": "Ember.js",
            "description": "Opinionated framework for ambitious web applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "backbone",
            "name": "Backbone.js",
            "description": "Lightweight JavaScript framework for structuring web applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "electron",
            "name": "Electron",
            "description": "Framework for building cross-platform desktop apps with JavaScript.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "cordova",
            "name": "Apache Cordova",
            "description": "Framework for building mobile apps with HTML, CSS and JavaScript.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "ionic",
            "name": "Ionic",
            "description": "Framework for building hybrid mobile and desktop apps with web technologies.",
            "kind": TechTagKind.FRAMEWORK.name,
        },
        {
            "id": uuid4(),
            "slug": "meteor",
            "name": "Meteor",
            "description": "Full-stack JavaScript framework for real-time web applications.",
            "kind": TechTagKind.FRAMEWORK.name,
        },

        # Tools / infrastructure
        {
            "id": uuid4(),
            "slug": "postgresql",
            "name": "PostgreSQL",
            "description": "Open source relational database, powerful and extensible.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "mysql",
            "name": "MySQL",
            "description": "Popular open source relational database for web applications.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "redis",
            "name": "Redis",
            "description": "In-memory key-value store for caching and messaging.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "docker",
            "name": "Docker",
            "description": "Containerization platform for packaging and running applications.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "kubernetes",
            "name": "Kubernetes",
            "description": "Container orchestration system for deploying and scaling services.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "aws",
            "name": "AWS",
            "description": "Amazon Web Services cloud platform.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "gcp",
            "name": "GCP",
            "description": "Google Cloud Platform services.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "azure",
            "name": "Azure",
            "description": "Microsoft Azure cloud platform.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "git",
            "name": "Git",
            "description": "Distributed version control system.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "linux",
            "name": "Linux",
            "description": "Operating system kernel and ecosystem widely used on servers.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "sqlalchemy",
            "name": "SQLAlchemy",
            "description": "Python SQL toolkit and ORM.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "alembic",
            "name": "Alembic",
            "description": "Database migration tool for SQLAlchemy.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "celery",
            "name": "Celery",
            "description": "Distributed task queue for Python.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "rabbitmq",
            "name": "RabbitMQ",
            "description": "Message broker for asynchronous communication.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "kafka",
            "name": "Apache Kafka",
            "description": "Distributed event streaming platform.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "github-actions",
            "name": "GitHub Actions",
            "description": "CI/CD platform integrated with GitHub.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "gitlab-ci",
            "name": "GitLab CI/CD",
            "description": "Built-in CI/CD system for GitLab.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "mongodb",
            "name": "MongoDB",
            "description": "Document-oriented NoSQL database.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "elasticsearch",
            "name": "Elasticsearch",
            "description": "Search and analytics engine.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "prometheus",
            "name": "Prometheus",
            "description": "Monitoring system and time series database.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "grafana",
            "name": "Grafana",
            "description": "Analytics and interactive visualization web application.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "influxdb",
            "name": "InfluxDB",
            "description": "Time series database for metrics and events.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "clickhouse",
            "name": "ClickHouse",
            "description": "Column-oriented OLAP database management system.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "sqlite",
            "name": "SQLite",
            "description": "Embedded relational database engine.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "mariadb",
            "name": "MariaDB",
            "description": "Community-developed fork of MySQL relational database.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "oracle-db",
            "name": "Oracle Database",
            "description": "Multi-model database management system produced by Oracle.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "snowflake",
            "name": "Snowflake",
            "description": "Cloud data platform for data warehousing.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "redshift",
            "name": "Amazon Redshift",
            "description": "Fully managed cloud data warehouse service.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "s3",
            "name": "Amazon S3",
            "description": "Object storage service from AWS.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "terraform",
            "name": "Terraform",
            "description": "Infrastructure as Code tool for provisioning cloud resources.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "ansible",
            "name": "Ansible",
            "description": "Automation tool for configuration management and deployment.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "helm",
            "name": "Helm",
            "description": "Package manager for Kubernetes applications.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "jenkins",
            "name": "Jenkins",
            "description": "Open-source automation server for CI/CD.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "travis-ci",
            "name": "Travis CI",
            "description": "Hosted continuous integration service for building and testing software.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "circleci",
            "name": "CircleCI",
            "description": "Continuous integration and delivery platform.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "pytest",
            "name": "pytest",
            "description": "Testing framework for Python.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "jest",
            "name": "Jest",
            "description": "Delightful JavaScript testing framework.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "cypress",
            "name": "Cypress",
            "description": "End-to-end testing framework for web applications.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "sentry",
            "name": "Sentry",
            "description": "Error tracking and performance monitoring platform.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "datadog",
            "name": "Datadog",
            "description": "Monitoring and security platform for cloud applications.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "nginx",
            "name": "Nginx",
            "description": "High-performance HTTP server and reverse proxy.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "apache-httpd",
            "name": "Apache HTTP Server",
            "description": "Widely-used open source web server.",
            "kind": TechTagKind.TOOL.name,
        },
        {
            "id": uuid4(),
            "slug": "loki",
            "name": "Loki",
            "description": "Log aggregation system inspired by Prometheus.",
            "kind": TechTagKind.TOOL.name,
        },
    ]


def upgrade() -> None:
    """Upgrade schema."""
    tech_tags_table = sa.table(
        "tech_tags",
        sa.column("id", sa.Uuid),
        sa.column("slug", sa.String(length=64)),
        sa.column("name", sa.String(length=128)),
        sa.column("description", sa.Text),
        sa.column(
            "kind",
            postgresql.ENUM(
                "LANGUAGE",
                "FRAMEWORK",
                "TOOL",
                name="techtagkind",
            ),
        ),
    )

    op.bulk_insert(tech_tags_table, _get_tech_tags_seed())


def downgrade() -> None:
    """Downgrade schema."""
    slugs = [tag["slug"] for tag in _get_tech_tags_seed()]
    op.execute(
        sa.text("DELETE FROM tech_tags WHERE slug = ANY(:slugs)").bindparams(
            sa.bindparam("slugs", slugs, sa.ARRAY(sa.String())),
        )
    )
