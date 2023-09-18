module.exports = {
	//mode: 'jit',	
	purge: ['./templates/**/*.html'],
	darkMode: false,
	theme: {
		colors: {
			transparent: 'transparent',
			current: 'currentColor',
			primary: '#F9BB5B',
			secondary: '#97D9F9',
			black: '#000000',
      gray: '#edf0f2',
			white: '#ffffff',
			red: '#a82122',
		},
		fontFamily: {
			primary: ['Nunito Sans', 'sans-serif'],
		},
		fontSize: {
			xs: ['0.75rem', '1rem'], // ['12px', '16px']
			sm: ['0.875rem', '1.125rem'], // ['14px', '18px'] (H5)
			base: ['1rem', '1.75rem'], // ['16px', '28px'] (body)
			md: ['1rem', '1.375rem'], // ['16px', '22px'] (H4)
			lg: ['1.25rem', '1.625rem'], // ['20px', '26px'] (H3)
			xl: ['1.5rem', '1.875rem'], // ['24px', '30px'] (H2)
			'1xl': ['1.75rem', '2.25rem'], // ['28px', '36px']  
			'2xl': ['2rem', '2.5rem'], // ['32px', '40px'] (H1)
			'3xl': ['2.625rem', '3rem'], // ['42px', '48px']  
		},
		fontWeight: {
			light: 300,
			normal: 400,
      semibold: 500,
			bold: 700,
		},
		screens: {
			xs: '30rem', // 480px
			md: '48rem', // 768px
			'lg-max': { max: '71.875rem' }, // 1023px
			lg: '71.875rem', // 1024px
			'xl-max': { max: '79.938rem' }, // 1279px
			xl: '80rem', // 1280px
		},
		container: {
			center: true,
			padding: {
				DEFAULT: '1rem', // 16px
				xl: '2.5rem', // 40px
			},
			screens: {
				DEFAULT: '100%',
				xl: '80rem', // 1280px
			},
		},
		extend: {
			boxShadow: {
				lg: '0 0 10px 0 rgba(0, 0, 0, 0.1)',
				xl: '0 0 20px 0 rgba(0, 0, 0, 0.1)',
				focus: 'inset 0 -2px 0 0 #009ee0',
			},
			minWidth: {
				body: '20rem',
			},
			maxWidth: {
				38: '9.5rem',
				62: '15.5rem',
				100: '25rem',
				content: '49.5rem',
				'8xl': '100rem',
				'9xl': '160rem',
			},
			minHeight: {
				9: '2.25rem',
				14: '3.5rem',
				70: '17.5rem',
				88: '22rem',
				150: '37.5rem',
				212: '53rem',
			},
			spacing: {
				30: '7.5rem',
				46: '11.5rem',
				53: '13.25rem',
			},
			zIndex: {
				45: '45',
				60: '60',
			},
		},
	},
	variants: {
		extend: {
			display: ['group-hover'],
			margin: ['group-hover, first, last'],
			padding: ['group-hover, first, last'],
			height: ['group-hover'],
			placeholderColor: ['group-hover'],
			gradientColorStops: ['group-hover'],
			visibility: ['group-hover'],
		},
	},
	plugins: [require('@tailwindcss/forms'),require('tailwindcss'), require('autoprefixer'), require('@tailwindcss/line-clamp')],
}
