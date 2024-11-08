"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LRUCache = void 0;
class LRUCache {
    constructor(capacity = 4096) {
        this.capacity = capacity;
        this.cache = new Map();
    }
    get(key) {
        const item = this.cache.get(key);
        if (item) {
            this.cache.delete(key);
            this.cache.set(key, item);
        }
        else {
            return undefined;
        }
        return item;
    }
    set(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        }
        else if (this.cache.size === this.capacity) {
            this.cache.delete(this.first());
        }
        this.cache.set(key, value);
    }
    first() {
        return this.cache.keys().next().value;
    }
}
exports.LRUCache = LRUCache;
//# sourceMappingURL=cache.js.map