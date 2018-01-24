import scala.swing._
import scala.swing.event._

object Editor extends SimpleSwingApplication {
	val textArea = new TextArea

	def top = new MainFrame {
		title = "Text Editor"

		contents = textArea

		listenTo(textArea.keys) 

		size = new Dimension(700, 700)
		centerOnScreen()

		def ctrlDown(mods:Int) = (1 == (1 & mods>>7))

		reactions += {
			case c @ KeyReleased(_, Key.S, mods, _) if ctrlDown(mods) =>  saveFile()
			case c @ KeyReleased(_, Key.O, mods, _) if ctrlDown(mods) =>  openFile()
		}

		menuBar = new MenuBar {
			contents += new Menu("File") {
				contents += new MenuItem(Action("Open") {
					openFile()
				})
				contents += new MenuItem(Action("Save") {
					saveFile()
				})
				contents += new Separator
				contents += new MenuItem(Action("Exit") {
					sys.exit(0)
				})
			}

			contents += new Menu("About") {
				contents += new MenuItem(Action("About") {
					val fr = new MainFrame {
						title = "About the Programmer"
						contents = new Label("Yusuf KILDAN, AGH Science and Technology")
						size = new Dimension(500,250)
						centerOnScreen()
					}
					fr.visible = true
				})
			}
		}
	}

	// MARK: - Functions

    def openFile() {
     	val chooser = new FileChooser
      	if (chooser.showOpenDialog(null) == FileChooser.Result.Approve) {
        	val source = scala.io.Source.fromFile(chooser.selectedFile)
        	textArea.text = source.mkString
        	source.close()
      }
    }

    def saveFile() {
      val chooser = new FileChooser
      if (chooser.showSaveDialog(null) == FileChooser.Result.Approve) {
        val pw = new java.io.PrintWriter(chooser.selectedFile)
        pw.print(textArea.text)
        pw.close()
      }

    }
}
