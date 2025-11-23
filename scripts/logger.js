import { CONFIG } from "./config.js";

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

const getLogLevel = () => {
  switch(CONFIG.ENV) {
    case 'DSV':
      return LOG_LEVELS.DEBUG; 
    case 'PRD':
      return LOG_LEVELS.WARN;  
    default:
      return LOG_LEVELS.DEBUG; 
  }
};

const CURRENT_LOG_LEVEL = getLogLevel();

class Logger {
  constructor(prefix = 'APP') {
    this.prefix = prefix;
  }

  debug(message, data = null) {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.DEBUG) {
      console.log(`🔵 [${this.prefix}] ${message}`, data || '');
    }
  }

  info(message, data = null) {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.INFO) {
      console.log(`🟢 [${this.prefix}] ${message}`, data || '');
    }
  }

  warn(message, data = null) {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.WARN) {
      console.warn(`🟡 [${this.prefix}] ${message}`, data || '');
    }
  }

  error(message, error = null) {
    if (CURRENT_LOG_LEVEL <= LOG_LEVELS.ERROR) {
      console.error(`🔴 [${this.prefix}] ${message}`, error || '');
    }
  }
}

export { Logger, LOG_LEVELS, CURRENT_LOG_LEVEL };

export const logger = new Logger('BACKGROUND');
export const titleLogger = new Logger('TITLE_VALIDATION');
export const tabLogger = new Logger('TAB_MONITOR');
export const storageLogger = new Logger('STORAGE');
export const apiLogger = new Logger('API');
export const authLogger = new Logger('AUTH');

logger.info(`Sistema de logs inicializado - Ambiente: ${CONFIG.ENV}, Nível: ${CURRENT_LOG_LEVEL}`);