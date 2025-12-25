#!/usr/bin/env node
/**
 * Export Excalidraw diagrams to PNG/SVG using Playwright.
 * Based on gatsby-embedder-excalidraw's approach of intercepting blob creation.
 *
 * Usage:
 *   node export_playwright.js input.excalidraw [output.png|output.svg]
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function exportDiagram(inputPath, outputPath) {
    const absoluteInput = path.resolve(inputPath);
    if (!fs.existsSync(absoluteInput)) {
        console.error(`Input file not found: ${absoluteInput}`);
        process.exit(1);
    }

    const diagramData = fs.readFileSync(absoluteInput, 'utf-8');
    const diagram = JSON.parse(diagramData);
    const absoluteOutput = path.resolve(outputPath || inputPath.replace(/\.excalidraw$/, '.png'));
    const exportSvg = absoluteOutput.endsWith('.svg');

    console.log(`Exporting: ${absoluteInput}`);
    console.log(`Output: ${absoluteOutput}`);

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1920, height: 1200 } });
    const page = await context.newPage();

    // Accept any dialogs
    page.on('dialog', dialog => dialog.accept());

    try {
        await page.goto('https://excalidraw.com/', { waitUntil: 'networkidle' });
        await page.waitForSelector('.excalidraw', { timeout: 30000 });
        await page.waitForTimeout(1500);

        // Load diagram via file drop
        const fileContent = JSON.stringify(diagram);
        await page.evaluate(async (content) => {
            const blob = new Blob([content], { type: 'application/json' });
            const file = new File([blob], 'diagram.excalidraw', { type: 'application/json' });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            document.querySelector('.excalidraw')?.dispatchEvent(
                new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer })
            );
        }, fileContent);

        await page.waitForTimeout(2000);

        // Fit view to content
        await page.keyboard.press('Shift+1');
        await page.waitForTimeout(500);

        await page.waitForTimeout(200);

        // Screenshot the canvas element
        const canvas = await page.$('canvas');
        if (canvas) {
            await canvas.screenshot({ path: absoluteOutput, omitBackground: false });
            console.log(`Exported via canvas screenshot: ${absoluteOutput}`);
        } else {
            // Fallback to page screenshot
            await page.screenshot({ path: absoluteOutput });
            console.log(`Exported via page screenshot: ${absoluteOutput}`);
        }

    } catch (error) {
        console.error('Export failed:', error.message);
        await page.screenshot({ path: '/tmp/excalidraw_debug.png' });
        console.log('Debug screenshot: /tmp/excalidraw_debug.png');
        throw error;
    } finally {
        await browser.close();
    }

    return absoluteOutput;
}

// CLI entry point
const args = process.argv.slice(2);
if (args.length < 1) {
    console.log('Usage: node export_playwright.js <input.excalidraw> [output.png]');
    process.exit(1);
}

exportDiagram(args[0], args[1])
    .then(output => {
        console.log('Done!');
        process.exit(0);
    })
    .catch(err => {
        console.error(err);
        process.exit(1);
    });
