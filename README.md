# 💰 Budget Calculator

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://microsoft.com/windows)

> A powerful, user-friendly desktop application for managing personal budgets and tracking expenses with intelligent categorization and comprehensive reporting.

## 🌟 Features

### 💡 Core Functionality
- **📊 Expense Tracking** - Add, edit, and delete expenses with detailed descriptions
- **🏷️ Smart Categorization** - Automatic expense categorization with custom keyword support
- **📈 Budget Management** - Set monthly budgets with visual progress indicators
- **🔍 Advanced Filtering** - Filter expenses by date range, category, and search terms
- **📋 Data Export** - Export data to Excel for further analysis
- **📊 Analytics** - Comprehensive expense analysis and reporting

### 🎨 User Experience
- **🌓 Theme Support** - Dark, Light, and System default themes
- **🌍 Multi-language** - English and Arabic support
- **⚡ Performance Optimized** - Fast database operations and smooth UI
- **💾 Data Persistence** - SQLite database for reliable data storage
- **📅 Start Month day** - User controls the start day of the month in settings general tab
- **🔧 Customizable** - Custom categories and settings

### 🛠️ Technical Features
- **Modern UI** - Built with PyQt5 for native look and feel
- **Cross-platform** - Windows, macOS, and Linux support
- **Portable** - Standalone executable with no installation required
- **Extensible** - Plugin architecture for custom features
- **Secure** - Local data storage with encryption options

## 📸 Screenshots

### Main Interface
![Main Interface](docs/screenshots/main-interface.png)
*Clean, intuitive interface with expense tracking and budget management*

### Custom Categories
![Custom Categories](docs/screenshots/custom-categories.png)
*Manage custom expense categories with keyword-based detection*

### Analytics Dashboard
![Analytics](docs/screenshots/analytics.png)
*Comprehensive expense analysis and reporting*

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

#### Option 1: From Source
```bash
# Clone the repository
git clone https://github.com/abdula8/trackyourbudget.git
cd budget-calculator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main_qt.py
```

#### Option 2: Pre-built Executable
1. Download the latest release from [Releases](https://github.com/abdula8/trackyourbudget/blob/main/BudgetCalculatorSetup.exe)
2. Run `BudgetCalculatorSetup.exe`
3. Follow the installation wizard

#### Option 3: Portable Version
1. Download the portable version
2. Extract to your desired location
3. Run `BudgetCalculator.exe`

## 📖 Usage

### Getting Started
1. **Set Your Budget** - Enter your monthly budget in the budget field
2. **Add Expenses** - Click "Add Expense" to record new expenses
3. **Use Auto-Categorization** - Select "Auto" to automatically categorize expenses
4. **Create Custom Categories** - Use "Manage Categories" for personalized categories
5. **Track Progress** - Monitor your spending with visual progress indicators

### Advanced Features
- **Filter Data** - Use date range, category, and search filters
- **Export Reports** - Export data to Excel for detailed analysis
- **Analyze Trends** - Use built-in analytics for spending insights
- **Customize Themes** - Choose from Dark, Light, or System themes

## 🛠️ Development

### Project Structure
```
budget-calculator/
├── main_qt.py              # Main application
├── analyze_expenses.py     # Expense analysis module
├── analyze_expenses_002.py # Excel export module
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── build.py              # Build automation script
├── installer.nsi         # NSIS installer script
├── docs/                 # Documentation
├── tests/                # Test files
└── resources/            # Icons and assets
```

### Setting Up Development Environment

1. **Clone and Setup**
   ```bash
   git clone https://github.com/abdula8/trackyourbudget.git
   cd budget-calculator
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Tests**
   ```bash
   python test_app.py
   ```

3. **Build Application**
   ```bash
   python build.py
   ```

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

#### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

#### Code Style
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Write comprehensive docstrings
- Include unit tests for new features

## 📋 Roadmap

### Version 2.0 (Planned)
- [ ] **Cloud Sync** - Synchronize data across devices
- [ ] **Mobile App** - Companion mobile application
- [ ] **Advanced Analytics** - Machine learning insights
- [ ] **Bill Reminders** - Automated bill tracking
- [ ] **Investment Tracking** - Portfolio management features

### Version 1.1 (Next Release)
- [ ] **Data Backup** - Automated backup system
- [ ] **Report Scheduling** - Automated report generation
- [ ] **Plugin System** - Third-party extensions
- [ ] **Advanced Filters** - More filtering options
- [ ] **Keyboard Shortcuts** - Power user features

## 🤝 Contributing

We love contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Report Bugs** - Use GitHub Issues
- 💡 **Suggest Features** - Open feature requests
- 📝 **Improve Documentation** - Help others understand the code
- 🔧 **Fix Issues** - Submit pull requests
- 🌍 **Translations** - Add new language support
- 🧪 **Testing** - Help test new features

### Development Setup
See [DEVELOPER.md](DEVELOPER.md) for detailed development instructions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🙏 Acknowledgments

- **PyQt5** - For the excellent GUI framework
- **SQLite** - For reliable data storage
- **Matplotlib** - For data visualization
- **Contributors** - Thank you to all contributors!

## 📞 Support

- **Documentation**: [Wiki](https://github.com/abdula8/trackyourbudget/wiki)
- **Issues**: [GitHub Issues](https://github.com/abdula8/trackyourbudget/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abdula8/trackyourbudget/discussions)
- **Email**: aabdallah.atef.0x@gmail.com

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=abdula8/trackyourbudget&type=Date)](https://star-history.com/#abdula8/trackyourbudget&Date)

---

<div align="center">
  <strong>Made with ❤️ for better financial management</strong>
</div>
