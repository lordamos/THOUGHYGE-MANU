import sharp from 'sharp';
import path from 'path';
import { promises as fs } from 'fs';

export class ImageOptimizer {
  constructor(options) {
    this.quality = options.quality || 80;
    this.formats = options.formats || ['webp', 'jpeg'];
    this.sizes = options.sizes || [800, 1200];
  }

  async optimizeImage(inputPath, outputDir) {
    const filename = path.basename(inputPath, path.extname(inputPath));
    const optimizedImages = [];

    for (const format of this.formats) {
      for (const size of this.sizes) {
        const outputPath = path.join(outputDir, `${filename}-${size}w.${format}`);
        let image = sharp(inputPath).resize(size);

        if (format === 'webp') {
          image = image.webp({ quality: this.quality });
        } else if (format === 'jpeg') {
          image = image.jpeg({ quality: this.quality });
        }

        await image.toFile(outputPath);
        optimizedImages.push({ filename: path.basename(outputPath), format, size });
      }
    }
    return optimizedImages;
  }
}


