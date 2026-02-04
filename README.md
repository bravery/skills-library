# Paper Insights Skill for OpenCode

This is an OpenCode skill for analyzing and summarizing AI/ML research papers. The skill provides comprehensive analysis of research papers including structured outputs, key contributions, method/experiment breakdowns, limitations, and reproduction notes.

## Overview

The Paper Insights skill is designed to:
- Analyze PDF research papers (from arXiv, conferences, etc.)
- Generate structured summaries with key contributions
- Break down methods and experiments
- Identify limitations and provide critique
- Offer reproduction notes
- Generate TL;DR summaries and deep analysis

## Skill Structure

```
paper-insights/
├── agents/           # Agent configuration files
├── references/       # Reference templates and outputs
├── scripts/          # Utility scripts (e.g., PDF text extraction)
└── SKILL.md          # Skill documentation
```

## Installation

### Prerequisites
- Node.js and npm installed
- OpenCode CLI
- Python 3.x (for PDF processing scripts)

### Install OpenCode

```bash
# Install OpenCode globally
npm install -g opencode
```

### Configure Skills Path

The skill should be placed in your OpenCode skills directory. By default, OpenCode looks for skills in:

- `~/.opencode/skills/` (user-specific)
- `/usr/local/share/opencode/skills/` (system-wide)

To add this directory as a skills path, update your OpenCode configuration:

```bash
# Create or update OpenCode config
mkdir -p ~/.opencode/
cat > ~/.opencode/config.json << 'EOF'
{
  "skillsPath": ["/Users/wangping/Documents/ai-coding/skills-lab/skills"]
}
EOF
```

### Install Python Dependencies

For PDF processing functionality, install the required Python packages:

```bash
# Install PDF processing dependencies
pip install pypdf pdfplumber
# or using requirements file if available
# pip install -r requirements.txt
```

## Usage

### Running the Skill in OpenCode

Once installed, you can use the skill through OpenCode's interface:

```bash
# Start OpenCode TUI
opencode

# Or run with a specific message
opencode run "请分析这篇关于Transformer架构的论文"

# You can also specify the agent explicitly
opencode run --agent paper-insights "请分析这份PDF论文"
```

### Using the Skill via CLI Commands

The skill provides several command-line utilities:

```bash
# Extract text from a PDF
python paper-insights/scripts/extract_pdf_text.py /path/to/paper.pdf --output extracted_text.txt

# Analyze a paper directly (if supported)
opencode run --agent paper-insights --input-pdf /path/to/paper.pdf --output-format deep-analysis
```

### Output Formats

The skill supports multiple output formats as defined in `paper-insights/references/output_templates.md`:
- Quick TL;DR (快速总结)
- Deep Analysis (深度分析)
- Review-Style Critique (综述式批评)
- Reproduction Notes (复现指南)

You can request specific formats in your prompts:
```
"请提供这篇论文的深度分析"
"请生成这篇论文的快速总结"
"请对这篇论文进行综述式批评"
```

## Key Features

1. **PDF Text Extraction**: Extracts text from PDF documents
2. **Structured Analysis**: Provides organized breakdown of paper components
3. **Critical Evaluation**: Identifies strengths and limitations
4. **Reproduction Guidance**: Offers notes for reproducing experiments
5. **Multiple Output Formats**: Generates various summary templates

## Configuration

Skill configuration is managed through the `opencode.json` file in the root directory.

## Dependencies

- OpenCode runtime environment
- Python scripts for PDF processing
- Custom agent configurations

## Development

### Setting Up Development Environment

```bash
# Clone or copy the skill directory
cp -r /path/to/skill ~/.opencode/skills/paper-insights

# Install dependencies
cd ~/.opencode/skills/paper-insights
pip install pypdf pdfplumber

# Test the PDF extraction script
python scripts/extract_pdf_text.py --help
```

### Adding New Features

This skill is part of the OpenCode ecosystem and is designed to be extensible. New analysis modules or output formats can be added as needed.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **PDF extraction fails**
   - Ensure `pypdf` or `pdfplumber` is installed
   - Check PDF is not password-protected or corrupted
   
2. **Skill not found**
   - Verify skills path is correctly set in OpenCode config
   - Ensure skill directory has proper README and SKILL.md files
   
3. **Memory issues with large PDFs**
   - Use `--pages-range` option in extract script
   - Process paper in sections if needed

## Support

- OpenType Documentation: https://opencode.ai/docs
- Issue Tracker: [GitHub Issues](https://github.com/anomalyco/opencode/issues)

## License

Part of the OpenCode project.