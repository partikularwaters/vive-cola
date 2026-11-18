// Cut the person out of a photo and save a transparent PNG, using Apple's
// Vision foreground mask (macOS 14 or later). Used by sync_assets.py for team
// photos shot on a plain background.
//
// Run: swift scripts/cutout.swift input.jpg output.png
import AppKit
import CoreImage
import Foundation
import Vision

let args = CommandLine.arguments
guard args.count == 3 else {
    FileHandle.standardError.write("usage: cutout.swift input output.png\n".data(using: .utf8)!)
    exit(2)
}
let input = URL(fileURLWithPath: args[1]), output = URL(fileURLWithPath: args[2])
guard let ci = CIImage(contentsOf: input, options: [.applyOrientationProperty: true]) else {
    FileHandle.standardError.write("unreadable image\n".data(using: .utf8)!)
    exit(1)
}
let handler = VNImageRequestHandler(ciImage: ci)
let request = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])
guard let result = request.results?.first else {
    FileHandle.standardError.write("no foreground found\n".data(using: .utf8)!)
    exit(1)
}
let buffer = try result.generateMaskedImage(ofInstances: result.allInstances, from: handler, croppedToInstancesExtent: false)
let masked = CIImage(cvPixelBuffer: buffer)
let context = CIContext()
try context.writePNGRepresentation(of: masked, to: output, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!)
