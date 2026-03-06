import { spawnSync } from 'node:child_process';

function run(args) {
  const result = spawnSync('npx', ['datocms', ...args], {
    stdio: 'inherit',
    shell: process.platform === 'win32',
  });

  if (result.status !== 0) {
    throw new Error(`Command failed: npx datocms ${args.join(' ')}`);
  }
}

const destination = process.argv[2];

if (!destination) {
  console.error('Usage: node scripts/datocms-release.mjs <destination-env-id>');
  process.exit(1);
}

try {
  run(['maintenance:on', '--force']);
  run(['migrations:run', `--destination=${destination}`]);
  run(['environments:promote', destination]);
} finally {
  try {
    run(['maintenance:off']);
  } catch (error) {
    console.error('Failed to disable maintenance mode.');
    console.error(error);
    process.exitCode = 1;
  }
}
