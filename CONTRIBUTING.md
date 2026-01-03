# Contributing to GroundedGeo

Thank you for your interest in contributing to GroundedGeo!

## Ways to Contribute

### 1. Report Issues
- Bug reports
- Dataset quality issues
- Documentation improvements

### 2. Submit Pull Requests
- New baseline implementations
- Evaluation metric improvements
- Documentation updates

### 3. Extend the Dataset
- Additional query buckets
- More geographic coverage
- New evidence sources

## Development Setup
```bash
git clone https://github.com/YOUR_USERNAME/groundedgeo.git
cd groundedgeo
pip install -r requirements.txt
```

## Code Style

- Python 3.8+ compatible
- Type hints encouraged
- Docstrings for public functions

## Dataset Contributions

If you want to add new queries:

1. Follow the existing schema in `data/groundedgeo_v1.0.json`
2. Ensure all required fields are present
3. Include at least one evidence span per query
4. Run validation: `python eval/validate.py`

## Questions?

Open an issue or contact the maintainers.
