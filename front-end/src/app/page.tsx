export default function Landing() {
	return (
		<div className='w-full h-screen bg-[#CBE5F6] flex flex-col items-center'>
			{/* Title */}
			<div className='text-[120px] font-normal text-[#0F3A57] mt-[68px] text-center'>
				mus(ai)c
			</div>

			{/* Subtitle */}
			<div className='text-[30px] font-normal text-[#185D8B] mt-[20px] text-center'>
				an ai-powered music application
			</div>

			{/* Buttons */}
			<div className='flex mt-[200px] space-x-[115px]'>
				{/* Login Box */}
				<div className='w-[440px] h-[167px] bg-[#63B0E3] flex items-center justify-center'>
					<div className='text-[50px] font-normal text-[#EEF6FC]'>login</div>
				</div>

				{/* Signup Box */}
				<div className='w-[440px] h-[167px] bg-[#97CAED] flex items-center justify-center'>
					<div className='text-[50px] font-normal text-[#185D8B]'>signup</div>
				</div>
			</div>
		</div>
	);
}
