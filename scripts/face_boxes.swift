// Print the largest face box in each image as JSON, using Apple's Vision framework.
// Used by sync_assets.py to place every team portrait's head at the same spot.
// Output per line: {"path": ..., "x": ..., "y": ..., "w": ..., "h": ...} in pixels,
// with y measured from the top of the image. Images with no face print null boxes.
//
// Run: swift scripts/face_boxes.swift image1.png image2.png ...
import Foundation
import Vision
import ImageIO

for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
        print("{\"path\": \"\(path)\", \"error\": \"unreadable\"}")
        continue
    }
    let request = VNDetectFaceRectanglesRequest()
    try? VNImageRequestHandler(cgImage: image, options: [:]).perform([request])
    let faces = (request.results ?? []).sorted { $0.boundingBox.width > $1.boundingBox.width }
    let W = Double(image.width), H = Double(image.height)
    if let f = faces.first {
        let b = f.boundingBox
        let x = b.minX * W, w = b.width * W, h = b.height * H
        let y = (1 - b.maxY) * H
        print("{\"path\": \"\(path)\", \"x\": \(Int(x)), \"y\": \(Int(y)), \"w\": \(Int(w)), \"h\": \(Int(h)), \"W\": \(Int(W)), \"H\": \(Int(H))}")
    } else {
        print("{\"path\": \"\(path)\", \"x\": null}")
    }
}
