export default function Page({ params }: { params: { slug: string } }) {
  return <div className='container'>Arg path: `{params.slug}`</div>
}
