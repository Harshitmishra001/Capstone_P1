# Mermaid Diagrams for Silent Witness LaTeX Report

Use these diagrams to generate PNG images for the `\includegraphics` placeholders in your LaTeX report.
You can view these directly in VS Code (using a Markdown Preview extension) or copy them into the [Mermaid Live Editor](https://mermaid.live/) to export them as PNGs. Save the exported images to an `images/` folder in your project directory.

## Figure 1: High-Level System Architecture (`images/architecture.png`)

```mermaid
flowchart TD
    subgraph Frontend [React / Vite / TypeScript]
        UI[Interactive Workspace]
        CP[Contradiction Panel]
        Map[Spatial / Temporal Views]
    end

    subgraph Backend [FastAPI]
        API[REST Endpoints /analyze]
    end

    subgraph ML_Core [ML Pipeline - Python]
        NER[Stage 1: spaCy NER & Negation]
        Ext[Stage 2: SmolLM Event Extraction]
        Clust[Stage 3: MiniLM Clustering]
        Detect[Stage 4: Contradiction Engine]
    end

    UI <-->|JSON Data| API
    API <--> ML_Core
    NER --> Ext --> Clust --> Detect
```

## Figure 2: Jev Hybrid Privacy Architecture (`images/jev_architecture.png`)

*(If you want to add this to Chapter 5)*

```mermaid
flowchart LR
    Raw[Raw Police Transcripts\nContains PII]

    subgraph Local_Machine [100% On-Premises Execution]
        SmolLM[SmolLM-3B\nEvent Extraction]
        Filter[PII Removal & Tuple Formatting]
    end

    subgraph Cloud [TypeSafe AI Cloud]
        Jev[Jev System One\nParallel Atomic Questions]
    end

    Raw --> SmolLM
    SmolLM -->|Tuples: Subject, Action, Object| Filter
    Filter -->|De-identified Claims\ne.g. 'robber wore red hoodie'| Jev
    Jev -->|Confidence Scores & Judgments| UI[FastAPI / React UI]
```

## Figure 3: The 5-Stage Pipeline (`images/pipeline.png`)

```mermaid
sequenceDiagram
    participant Doc as Raw Transcripts
    participant Stage1 as spaCy (NER)
    participant Stage2 as SmolLM (Extraction)
    participant Stage3 as MiniLM (Clustering)
    participant Stage4 as Contradiction Engine
    
    Doc->>Stage1: Ingest Text
    Stage1->>Stage2: Scoped Entities & Timestamps
    Stage2->>Stage3: (Subj, Action, Obj) Tuples
    Stage3->>Stage4: Pruned Thematic Pairs (-90% O(N^2))
    Stage4->>Doc: Verified JSON Output
```
