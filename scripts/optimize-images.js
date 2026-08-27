#!/usr/bin/env node

/**
 * Image Optimization Build Script
 * Run this script to optimize all images in the public/images directory
 * Usage: node scripts/optimize-images.js
 */

import { ImageOptimizer } from '../src/utils/imageOptimization.js';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PROJECT_ROOT = path.resolve(__dirname, '..');
const INPUT_DIR = path.join(PROJECT_ROOT, 'public', 'images');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'public', 'images', 'optimized');

async function main() {
  console.log('🖼️  Starting image optimization...');
  console.log(`Input directory: ${INPUT_DIR}`);
  console.log(`Output directory: ${OUTPUT_DIR}`);

  try {
    // Check if input directory exists
    try {
      await fs.access(INPUT_DIR);
    } catch (error) {
      console.log('📁 Creating images directory...');
      await fs.mkdir(INPUT_DIR, { recursive: true });
      console.log('ℹ️  No images found to optimize. Add images to public/images/ directory.');
      return;
    }

    // Create output directory
    await fs.mkdir(OUTPUT_DIR, { recursive: true });

    // Initialize optimizer
    const optimizer = new ImageOptimizer({
      quality: 85,
      formats: ['webp', 'jpeg'],
      sizes: [400, 800, 1200, 1600]
    });

    // Get all image files
    const getImageFiles = async (dir) => {
      let files = [];
      const items = await fs.readdir(dir, { withFileTypes: true });

      for (const item of items) {
        if (item.isDirectory()) {
          files = [...files, ...(await getImageFiles(path.join(dir, item.name)))];
        } else if (/\.(jpg|jpeg|png|webp|tiff)$/i.test(item.name) && !item.name.startsWith(".")) {
          files.push(path.join(dir, item.name));
        }
      }
      return files;
    };

    const imageFiles = await getImageFiles(INPUT_DIR);
    const relativeImageFiles = imageFiles.map(file => path.relative(INPUT_DIR, file));

    if (imageFiles.length === 0) {
      console.log('ℹ️  No images found to optimize.');
      return;
    }

    console.log(`📸 Found ${imageFiles.length} images to optimize:`);
    relativeImageFiles.forEach(file => console.log(`   - ${file}`));

    let totalOptimized = 0;

    // Optimize each image
    for (const inputPath of imageFiles) {
      console.log(`\n🔄 Optimizing ${path.relative(PROJECT_ROOT, inputPath)}...`);
      
      const relativePath = path.relative(INPUT_DIR, inputPath);
      const outputSubDir = path.join(OUTPUT_DIR, path.dirname(relativePath));
      await fs.mkdir(outputSubDir, { recursive: true });

      const optimizedImages = await optimizer.optimizeImage(inputPath, outputSubDir);
      
      console.log(`   ✅ Generated ${optimizedImages.length} optimized versions`);
      optimizedImages.forEach(img => {
        console.log(`      - ${img.filename} (${img.format}, ${img.size}w)`);
      });
      
      totalOptimized += optimizedImages.length;
    }

    console.log(`\n🎉 Optimization complete!`);
    console.log(`📊 Summary:`);
    console.log(`   - Original images: ${imageFiles.length}`);
    console.log(`   - Optimized versions: ${totalOptimized}`);
    console.log(`   - Output directory: ${OUTPUT_DIR}`);

    // Generate usage examples
    console.log(`\n📝 Usage examples:`);
    console.log(`   In your Astro components, use optimized images like:`);
    imageFiles.forEach(file => {
      const basename = path.basename(file, path.extname(file));
      console.log(`   <img src="/images/optimized/${basename}-800w.webp" alt="Description" />`);
    });

  } catch (error) {
    console.error('❌ Error during optimization:', error);
    process.exit(1);
  }
}

// Run the script
main().catch(console.error);

