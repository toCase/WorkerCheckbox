import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Controls.Fusion
import QtQuick.Layouts
import QtQuick.Dialogs

Item {

    QtObject {
        id: internal

        function selectFile(file){
            file_name.text = xls.url_name(file)
            var r = xls.get_data(file_name.text)
            console.info(r)

            if (r[0] === 1){
                // modelOrder.loadModel(2)
                orderNorm.load()
                orderTTN.load()
            }
        }
    }


    ColumnLayout {
        anchors.fill: parent

        spacing: 10

        RowLayout {
            id: menu_file
            Layout.fillWidth: true
            Layout.maximumHeight: 35
            Layout.minimumHeight: 35


            Label {
                id: label
                text: qsTr("Файл:")
                font.pointSize: 11
            }

            TextField {
                id: file_name
                readOnly: true
                Layout.fillWidth: true
                Layout.fillHeight: true
                placeholderText: qsTr("Select file")
            }

            Button {
                id: but_select
                Layout.maximumWidth: 40
                Layout.fillHeight: true
                text: qsTr("...")
                onClicked: {
                    timerOff()
                    fileDialog.open()
                }
            }

        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true

            OrderNormal {
                id: orderNorm
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Rectangle {
                Layout.minimumWidth: 2
                Layout.maximumWidth: 2
                Layout.fillHeight: true
                color: "#32bd68"

            }

            OrderTTN {
                id: orderTTN
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }

    FileDialog {
        id: fileDialog
        fileMode: FileDialog.OpenFile
        currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
        nameFilters: ["Excel files (*.xlsx)"]
        onAccepted: {
            internal.selectFile(selectedFile)
        }
    }

}
