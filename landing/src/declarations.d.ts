declare var document: any;
declare var window: any;
declare var HTMLElement: any;

declare namespace React {
  export type FC<P = {}> = (props: P) => any;
  export type FunctionComponent<P = {}> = (props: P) => any;
  export type ReactNode = any;
  export type CSSProperties = Record<string, any>;
  export interface ReactElement<P = any, T = any> {
    type: T;
    props: P;
    key: any;
  }
  export interface Component<P = {}, S = {}> {}
  export function useState<T>(initialState: T | (() => T)): [T, (newState: T | ((prevState: T) => T)) => void];
  export function useEffect(effect: () => void | (() => void), deps?: readonly any[]): void;
  export function useRef<T>(initialValue?: T): { current: T };
  export function useMemo<T>(factory: () => T, deps: readonly any[] | undefined): T;
  export function useCallback<T extends (...args: any[]) => any>(callback: T, deps: readonly any[]): T;
  export function createElement(type: any, props?: any, ...children: any[]): any;
  export const StrictMode: any;
}

declare module 'react' {
  export = React;
  export as namespace React;
}

declare module 'react/jsx-runtime' {
  export const jsx: any;
  export const jsxs: any;
  export const Fragment: any;
}

declare module 'react-dom/client' {
  export function createRoot(container: any): {
    render(children: any): void;
    unmount(): void;
  };
}

declare module 'lucide-react' {
  export const ArrowRight: any;
  export const Menu: any;
  export const X: any;
  export const Layers: any;
  export const Database: any;
  export const Cpu: any;
  export const ShieldCheck: any;
  export const Terminal: any;
  export const Play: any;
  export const AlertCircle: any;
  export const ExternalLink: any;
  export const Zap: any;
  export const CheckCircle2: any;
  export const XCircle: any;
  export const AlertTriangle: any;
  export const Check: any;
  export const Microscope: any;
  export const TrendingUp: any;
  export const GraduationCap: any;
  const LucideIcons: Record<string, any>;
  export default LucideIcons;
}

declare module 'vite' {
  export function defineConfig(config: any): any;
}

declare module '@vitejs/plugin-react' {
  const plugin: any;
  export default plugin;
}

declare global {
  namespace JSX {
    interface Element {
      [key: string]: any;
    }
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
}
