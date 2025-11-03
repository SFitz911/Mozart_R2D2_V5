"""
Mozart R2D2 V5 - DeepSeek Coder Launcher
GUI for launching local or remote DeepSeek Coder instances
Supports both simple and chat-based interfaces
"""

import sys
import os
import subprocess
import threading
from pathlib import Path

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QTextEdit, QLabel, QComboBox, QSpinBox, QCheckBox,
        QProgressBar, QGroupBox, QFileDialog, QMessageBox
    )
    from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer
    from PyQt5.QtGui import QFont, QColor
except ImportError:
    print("❌ PyQt5 not installed. Install it with: pip install PyQt5")
    sys.exit(1)


class Worker(QThread):
    """Thread worker for running commands without blocking UI"""
    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    progress_signal = pyqtSignal(int)

    def __init__(self, command, description=""):
        super().__init__()
        self.command = command
        self.description = description

    def run(self):
        try:
            self.log_signal.emit(f"\n{'='*60}\n🚀 {self.description}\n{'='*60}\n")
            
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            
            for line in process.stdout:
                self.log_signal.emit(line.rstrip('\n'))
            
            process.wait()
            
            if process.returncode == 0:
                self.log_signal.emit(f"\n✅ {self.description} completed successfully!")
            else:
                self.error_signal.emit(f"❌ {self.description} failed with code {process.returncode}")
            
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(f"❌ Error: {str(e)}")
            self.finished_signal.emit()


class Launcher(QMainWindow):
    """Main launcher GUI"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        self.setStyleSheet(self._get_stylesheet())

    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("🤖 Mozart R2D2 V5 - DeepSeek Coder Launcher")
        self.setGeometry(100, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("🚀 DeepSeek Coder Launcher")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        main_layout.addWidget(header)

        # Mode selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Select Interface:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "💬 Modern Chat Interface (Recommended)",
            "📝 Simple Text Interface",
        ])
        self.mode_combo.setCurrentIndex(0)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)

        # Setup options
        setup_group = QGroupBox("⚙️ Setup Options")
        setup_layout = QVBoxLayout()

        self.download_model_btn = QPushButton("📥 Download Model")
        self.download_model_btn.clicked.connect(self.download_model)
        setup_layout.addWidget(self.download_model_btn)

        self.install_deps_btn = QPushButton("📦 Install Dependencies")
        self.install_deps_btn.clicked.connect(self.install_dependencies)
        setup_layout.addWidget(self.install_deps_btn)

        setup_group.setLayout(setup_layout)
        main_layout.addWidget(setup_group)

        # Launch options
        launch_group = QGroupBox("🚀 Launch Options")
        launch_layout = QVBoxLayout()

        with_share_layout = QHBoxLayout()
        self.share_checkbox = QCheckBox("Enable Gradio Share Link (public access)")
        self.share_checkbox.setChecked(True)
        with_share_layout.addWidget(self.share_checkbox)
        with_share_layout.addStretch()
        launch_layout.addLayout(with_share_layout)

        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_spin = QSpinBox()
        self.port_spin.setValue(7860)
        self.port_spin.setMinimum(1024)
        self.port_spin.setMaximum(65535)
        port_layout.addWidget(self.port_spin)
        port_layout.addStretch()
        launch_layout.addLayout(port_layout)

        self.launch_btn = QPushButton("▶️ Launch Application")
        self.launch_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.launch_btn.clicked.connect(self.launch_app)
        launch_layout.addWidget(self.launch_btn)

        launch_group.setLayout(launch_layout)
        main_layout.addWidget(launch_group)

        # Log window
        log_group = QGroupBox("📋 Log Output")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #30363d;
                border-radius: 5px;
                background-color: #161b22;
            }
            QProgressBar::chunk {
                background-color: #58a6ff;
            }
        """)
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        # Status label
        self.status_label = QLabel("✅ Ready")
        main_layout.addWidget(self.status_label)

    def _get_stylesheet(self):
        """Return custom stylesheet for dark theme"""
        return """
        QMainWindow {
            background-color: #010409;
        }
        QLabel {
            color: #c9d1d9;
        }
        QPushButton {
            background-color: #58a6ff;
            color: #010409;
            border: none;
            border-radius: 5px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #79c0ff;
        }
        QPushButton:pressed {
            background-color: #388bfd;
        }
        QTextEdit {
            background-color: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 5px;
        }
        QComboBox, QSpinBox {
            background-color: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 5px;
            padding: 5px;
        }
        QCheckBox {
            color: #c9d1d9;
        }
        QGroupBox {
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        """

    def log(self, message):
        """Add message to log window"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def download_model(self):
        """Download DeepSeek Coder model"""
        self.disable_buttons()
        cmd = "huggingface-cli download deepseek-ai/deepseek-coder-1.3b-instruct --local-dir models/deepseek-coder-1.3b-instruct"
        self.run_worker(cmd, "Downloading DeepSeek Coder model...")

    def install_dependencies(self):
        """Install Python dependencies"""
        self.disable_buttons()
        cmd = f"{sys.executable} -m pip install -r requirements.txt"
        self.run_worker(cmd, "Installing dependencies...")

    def launch_app(self):
        """Launch the application"""
        self.disable_buttons()
        
        mode_index = self.mode_combo.currentIndex()
        port = self.port_spin.value()
        share = "--share" if self.share_checkbox.isChecked() else ""
        
        if mode_index == 0:
            # Modern chat interface
            cmd = f"{sys.executable} chat_app.py --port {port} {share}"
            description = "Launching Modern Chat Interface..."
        else:
            # Simple interface
            cmd = f"{sys.executable} app.py --port {port} {share}"
            description = "Launching Simple Interface..."
        
        self.run_worker(cmd, description)

    def run_worker(self, command, description):
        """Run a command in a worker thread"""
        self.worker = Worker(command, description)
        self.worker.log_signal.connect(self.log)
        self.worker.error_signal.connect(self.show_error)
        self.worker.finished_signal.connect(self.enable_buttons)
        self.worker.start()

    def disable_buttons(self):
        """Disable all action buttons"""
        self.download_model_btn.setEnabled(False)
        self.install_deps_btn.setEnabled(False)
        self.launch_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setMaximum(0)  # Indeterminate progress
        self.status_label.setText("⏳ Running...")

    def enable_buttons(self):
        """Enable all action buttons"""
        self.download_model_btn.setEnabled(True)
        self.install_deps_btn.setEnabled(True)
        self.launch_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.status_label.setText("✅ Ready")

    def show_error(self, message):
        """Show error dialog"""
        QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec_())
