/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				// Brand accent (#C05B28 burnt sienna)
				brand: {
					50:  '#fdf5f0',
					100: '#fae4d5',
					600: '#C05B28',
					700: '#a34d22',
					800: '#87401c'
				},
				// Status colors
				status: {
					completed: '#16a34a',
					pending: '#d97706',
					failed: '#dc2626',
					canceled: '#dc2626'
				},
				// Department accent (subtle)
				dept: {
					sales: '#3b82f6',
					engineering: '#8b5cf6',
					support: '#06b6d4',
					IT: '#f59e0b',
					product_management: '#ec4899',
					marketing: '#f97316',
					'r&d': '#10b981',
					accounting: '#6366f1',
					hr: '#14b8a6',
					management: '#64748b'
				}
			},
			fontFamily: {
				sans: ['Plus Jakarta Sans', 'system-ui', 'sans-serif']
			},
			animation: {
				'slide-in': 'slideIn 0.2s ease-out',
				'fade-in': 'fadeIn 0.15s ease-out'
			},
			keyframes: {
				slideIn: {
					'0%': { transform: 'translateX(-8px)', opacity: '0' },
					'100%': { transform: 'translateX(0)', opacity: '1' }
				},
				fadeIn: {
					'0%': { opacity: '0' },
					'100%': { opacity: '1' }
				}
			}
		}
	},
	plugins: [require('@tailwindcss/typography')]
};
