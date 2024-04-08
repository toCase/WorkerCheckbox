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
                modelOrder.loadModel(2)
            }
        }
    }


    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        spacing: 10

        RowLayout {
            id: rowLayout
            Layout.fillWidth: true
            Layout.maximumHeight: 35
            Layout.minimumHeight: 35


            Label {
                id: label
                text: qsTr("File:")
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
                onClicked: fileDialog.open()
            }

        }


        ListView {
            id: table
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: modelOrder
            clip: true
            // delegate: rowDelegate
            delegate: Item {

                width: table.width
                implicitHeight: itemCol.implicitHeight


                ColumnLayout{
                    id: itemCol
                    anchors.fill: parent

                    RowLayout {
                        Layout.fillWidth: true
                        Layout.minimumHeight: 35
                        Layout.maximumHeight: 35
                        spacing: 10

                        Label {
                            Layout.minimumWidth: 80
                            Layout.maximumWidth: 80
                            text: id
                        }

                        Label {
                            Layout.minimumWidth: 180
                            Layout.maximumWidth: 180
                            text: phone
                        }
                        Label {
                            Layout.minimumWidth: 180
                            Layout.maximumWidth: 180
                            text: ttn
                        }
                        Item {
                            Layout.fillWidth: true
                        }
                    }

                    Repeater {
                        Layout.fillWidth: true
                        implicitHeight: detailEl.implicitHeight
                        model: base.detail_getX(id)

                        Text {
                            id: detailEl
                            height: 20

                            required property string modelData
                            text: modelData
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.minimumHeight: 2
                        Layout.maximumHeight: 2

                        color: "#660066"
                    }

                }
            }
        }
        RowLayout {
            id: rowLayout1
            width: 100
            height: 100
            Item {
                Layout.fillWidth: true
                visible: !progressBar.visible
            }

            ProgressBar {
                id: progressBar
                visible: false
                height: 15
                value: 0.5
                Layout.fillWidth: true
            }

            Button {
                id: but_load
                text: qsTr("load to RRO")
                onClicked: {
                    progressBar.visible = !progressBar.visible
                }
            }
        }
    }

    // Item {
    //     id: rowDelegate
    //     width: table.width
    //     height: 50

    //     ColumnLayout {
    //         anchors.fill: parent
    //         spacing: 10

    //         RowLayout {
    //             anchors.fill: parent
    //             spacing: 10
    //             Label {
    //                 Layout.minimumWidth: 80
    //                 Layout.maximumWidth: 80
    //                 text: id
    //             }

    //             Label {
    //                 Layout.minimumWidth: 180
    //                 Layout.maximumWidth: 180
    //                 text: phone
    //             }
    //             Label {
    //                 Layout.minimumWidth: 180
    //                 Layout.maximumWidth: 180
    //                 text: ttn
    //             }
    //             Item {
    //                 Layout.fillWidth: true
    //             }
    //         }

    //         // Column {
    //         //     Repeater {
    //         //         model: detail
    //         //         Text {
    //         //             required property string modelData
    //         //             text: "Data: " + modelData
    //         //         }
    //         //     }
    //         // }

    //     }

    // }


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
