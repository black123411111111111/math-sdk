# Stake Engine Math SDK

Welcome to [Stake Engine Math SDK](https://engine.stake.com/)!

The Math SDK is a Python-based engine for defining game rules, simulating outcomes, and optimizing win distributions. It generates all necessary backend and configuration files, lookup tables, and simulation results.

## Web SDK Integration

This repository now includes a **Web SDK** for frontend integration:

- **Location**: `/web-sdk/`
- **Language**: TypeScript/JavaScript
- **Framework**: Framework-agnostic (works with React, Vue, Svelte, etc.)
- **Purpose**: Connects web frontends to the Stake Engine RGS

### Quick Start with Web SDK

```bash
cd web-sdk
npm install
npm run build

# Run the example
cd examples/simple-game
npm install
npm run dev
```

For complete Web SDK documentation, see [`web-sdk/README.md`](web-sdk/README.md) and [`docs/web_sdk_integration.md`](docs/web_sdk_integration.md).

## Math SDK Documentation
   
For technical details [view the docs](https://stakeengine.github.io/math-sdk/)


# Installation
 
This repository requires Python3 (version >= 3.12), along with the PIP package installer.
If the included optimization algorithm is being used, Rust/Cargo will also need to be installed.

It is recommended to use [Make](https://www.gnu.org/software/make/) and setup the engine by running:
```sh
make setup
```

Alternatively, visit our [Setup and Installation page](https://stakeengine.github.io/math-sdk/math_docs/general_overview/) for more details.

